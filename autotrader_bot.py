#!/usr/bin/env python3
"""
AutoTrader.ca notifier ‒ GitHub-Actions friendly

Changes
▪ switch scraper to Playwright (handles AutoTrader.ca’s JS-rendered listings)
▪ robust selectors for CA site
▪ graceful fall-back / logging
"""

import hashlib
import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from twilio.rest import Client
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

### ---------- config & helpers ------------------------------------------------
REPO_ROOT = Path(__file__).parent
SEEN_FILE = REPO_ROOT / "seen_listings.json"
ARCHIVE_DIR = REPO_ROOT / "archives"

REQUIRED_ENV = [
    "SEARCH_URL",
    "GMAIL_USER",
    "GMAIL_APP_PASSWORD",
    "TWILIO_SID",
    "TWILIO_TOKEN",
    "TWILIO_FROM",
    "TWILIO_TO",
]

def load_env() -> None:
    load_dotenv()
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        print(f"[fatal] Missing env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

def load_seen() -> set:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()

def save_seen(seen: set) -> None:
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2))

def sha10(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:10]

### ---------- scraping --------------------------------------------------------

def fetch_listings(url: str) -> List[Dict]:
    """
    Uses Playwright (headless Chromium) because AutoTrader.ca injects listings
    client-side.  We wait for the listing cards, then pull id, title, href.
    """
    print(f"Fetching {url} ...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60_000)
            page.wait_for_selector('[data-qaid="cntnr-listing-card"]',
                                   timeout=15_000)
        except PWTimeout:
            print("[warn] No listing cards found (timeout) – site layout "
                  "may have changed.")
            return []
        cards = page.query_selector_all('[data-qaid="cntnr-listing-card"]')
        listings = []
        for c in cards:
            lid = c.get_attribute("data-listing-id")
            # some cards (e.g. ads) miss this attr → skip
            if not lid:
                continue
            title_el = c.query_selector('[data-qaid="card-title"]')
            title = title_el.inner_text().strip() if title_el else "Untitled"
            link_el = c.query_selector("a")
            href = ("https://www.autotrader.ca"
                    + link_el.get_attribute("href")) if link_el else url
            listings.append({"id": lid, "title": title, "url": href})
        browser.close()
        print(f"Parsed {len(listings)} listings.")
        return listings

### ---------- notifications ---------------------------------------------------

def send_email(subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
        smtp.sendmail(msg["From"], [msg["To"]], msg.as_string())

def send_sms(body: str) -> None:
    cli = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    cli.messages.create(
        body=body,
        from_=os.getenv("TWILIO_FROM"),
        to=os.getenv("TWILIO_TO"),
    )

def notify(listing: Dict) -> None:
    text = f"{listing['title']}\n{listing['url']}"
    send_email("New AutoTrader listing", text)
    send_sms(text)

### ---------- archiving -------------------------------------------------------

def archive(listing: Dict) -> None:
    slug = sha10(listing["id"])
    dest = ARCHIVE_DIR / slug
    dest.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": listing["id"],
        "title": listing["title"],
        "url": listing["url"],
        "fetched": datetime.utcnow().isoformat(timespec="seconds"),
    }
    (dest / "metadata.json").write_text(json.dumps(meta, indent=2))

### ---------- main ------------------------------------------------------------

def main() -> None:
    load_env()
    seen = load_seen()
    listings = fetch_listings(os.getenv("SEARCH_URL"))
    new = [x for x in listings if x["id"] not in seen]
    print(f"Found {len(new)} new listings (seen cache: {len(seen)})")
    for lst in new:
        try:
            notify(lst)
            archive(lst)
            seen.add(lst["id"])
        except Exception as exc:
            print(f"[err] failed processing {lst['id']}: {exc}", file=sys.stderr)
    save_seen(seen)
    print("Done.")

if __name__ == "__main__":
    main()
