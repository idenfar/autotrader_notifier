#!/usr/bin/env python3
"""
AutoTrader.ca notifier – with optional DEBUG diagnostics.

If DEBUG=true is set in env, the script will:
▪ capture Playwright console messages
▪ dump the final DOM to archives/_debug/<timestamp>/dom.html
▪ take a full-page screenshot to …/screenshot.png

These artifacts are committed by the Action so you can inspect them
in the repo after a run.
"""

import hashlib, json, os, smtplib, sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from twilio.rest import Client
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ---------- configuration ----------------------------------------------------

ROOT          = Path(__file__).parent
SEEN_FILE     = ROOT / "seen_listings.json"
ARCHIVE_DIR   = ROOT / "archives"
DEBUG_MODE    = os.getenv("DEBUG", "false").lower() == "true"

REQ_VARS = [
    "SEARCH_URL", "GMAIL_USER", "GMAIL_APP_PASSWORD",
    "TWILIO_SID", "TWILIO_TOKEN", "TWILIO_FROM", "TWILIO_TO",
]

def need_env():
    load_dotenv()
    miss = [k for k in REQ_VARS if not os.getenv(k)]
    if miss:
        print(f"[fatal] missing env vars: {', '.join(miss)}", file=sys.stderr)
        sys.exit(1)

def load_seen() -> set:
    return set(json.loads(SEEN_FILE.read_text())) if SEEN_FILE.exists() else set()

def save_seen(seen: set):
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2))

def sha10(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:10]

# ---------- scraping ---------------------------------------------------------

def make_debug_dir() -> Path:
    utc = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    d   = ARCHIVE_DIR / "_debug" / utc
    d.mkdir(parents=True, exist_ok=True)
    return d

def fetch_listings(url: str) -> List[Dict]:
    """
    Return list of dict(id,title,url).  If DEBUG_MODE, capture console logs,
    page DOM, and screenshot.
    """
    print(f"Fetching {url} …")
    debug_dir   = make_debug_dir() if DEBUG_MODE else None
    console_buf = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page    = browser.new_page()

        if DEBUG_MODE:
            page.on("console", lambda m: console_buf.append(m.text()))

        try:
            page.goto(url, timeout=60_000)
            page.wait_for_selector('[data-qaid="cntnr-listing-card"]',
                                   timeout=15_000)
        except PWTimeout:
            print("[warn] No listing cards found (timeout).")
        cards = page.query_selector_all('[data-qaid="cntnr-listing-card"]')
        print(f"[info] query_selector_all returned {len(cards)} cards.")

        listings = []
        for c in cards:
            lid = c.get_attribute("data-listing-id")
            if not lid:
                continue
            title_el = c.query_selector('[data-qaid="card-title"]')
            title    = title_el.inner_text().strip() if title_el else "Untitled"
            link_el  = c.query_selector("a")
            href     = ("https://www.autotrader.ca"
                        + link_el.get_attribute("href")) if link_el else url
            listings.append({"id": lid, "title": title, "url": href})

        # ---- debug artifacts -------------------------------------------------
        if DEBUG_MODE:
            if console_buf:
                (debug_dir / "console.log").write_text(
                    "\n".join(console_buf), encoding="utf-8")
            (debug_dir / "dom.html").write_text(
                page.content(), encoding="utf-8")
            page.screenshot(path=str(debug_dir / "screenshot.png"),
                            full_page=True)
            print(f"[debug] wrote DOM/screenshot to {debug_dir.relative_to(ROOT)}")

        browser.close()
        return listings

# ---------- notifications ----------------------------------------------------

def send_email(subj: str, body: str):
    msg         = MIMEText(body)
    msg["From"] = msg["To"] = os.getenv("GMAIL_USER")
    msg["Subject"] = subj
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())

def send_sms(body: str):
    c = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    c.messages.create(body=body,
                      from_=os.getenv("TWILIO_FROM"),
                      to=os.getenv("TWILIO_TO"))

def notify(item: Dict):
    txt = f"{item['title']}\n{item['url']}"
    send_email("New AutoTrader listing", txt)
    send_sms(txt)

# ---------- archiving --------------------------------------------------------

def archive(item: Dict):
    d = ARCHIVE_DIR / sha10(item["id"])
    d.mkdir(parents=True, exist_ok=True)
    meta = {
        **item,
        "fetched": datetime.utcnow().isoformat(timespec="seconds"),
    }
    (d / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

# ---------- main -------------------------------------------------------------

def main():
    need_env()
    seen = load_seen()
    new  = [x for x in fetch_listings(os.getenv("SEARCH_URL"))
            if x["id"] not in seen]
    print(f"Found {len(new)} new listings (seen cache: {len(seen)})")

    for item in new:
        try:
            notify(item)
            archive(item)
            seen.add(item["id"])
        except Exception as e:
            print(f"[err] failed on {item['id']}: {e}", file=sys.stderr)

    save_seen(seen)
    print("Done.")

if __name__ == "__main__":
    main()
