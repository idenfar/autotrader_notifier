#!/usr/bin/env python3
"""Simple AutoTrader notifier.

Fetches search results from AutoTrader and sends notifications via
Gmail and Twilio for new listings. Credentials and configuration are
read from environment variables or a .env file.
"""
from __future__ import annotations

import json
import os
import sys
from email.mime.text import MIMEText
from pathlib import Path
import hashlib

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from twilio.rest import Client

# Mapping of required environment variables and friendly descriptions
ENV_VARS = {
    "SEARCH_URL": "AutoTrader search results URL",
    "GMAIL_USER": "Gmail address",
    "GMAIL_APP_PASSWORD": "Gmail app password",
    "TWILIO_SID": "Twilio account SID",
    "TWILIO_TOKEN": "Twilio auth token",
    "TWILIO_FROM": "Twilio 'from' phone number",
    "TWILIO_TO": "Destination phone number",
}

SEEN_FILE = Path("seen_listings.json")
ARCHIVE_DIR = Path("archives")


def interactive_setup() -> None:
    """Prompt the user for credentials and save them to .env."""
    print("Interactive setup for AutoTrader notifier.\nValues will be written to .env")
    if Path(".env").exists():
        ans = input(".env already exists. Overwrite? [y/N]: ").strip().lower()
        if ans != "y":
            print("Setup aborted.")
            return
    lines = []
    for key, desc in ENV_VARS.items():
        value = input(f"{desc} ({key}): ").strip()
        lines.append(f"{key}={value}")
    Path(".env").write_text("\n".join(lines))
    print(".env file written.")


def load_config() -> dict:
    """Load environment variables and ensure all are present."""
    load_dotenv()
    config = {}
    missing = []
    for key in ENV_VARS:
        val = os.getenv(key)
        if not val:
            missing.append(key)
        config[key] = val
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    return config


def load_seen() -> set[str]:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except json.JSONDecodeError:
            return set()
    return set()


def save_seen(seen: set[str]) -> None:
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2))


def _hash_id(text: str) -> str:
    """Return a short hash for use as a directory name."""
    return hashlib.sha1(text.encode()).hexdigest()[:10]


def archive_listing(listing: dict) -> None:
    """Download the listing page and images under ARCHIVE_DIR."""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(listing["url"], headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to fetch {listing['url']}: {exc}")
        return

    lid = _hash_id(listing["url"])
    listing_dir = ARCHIVE_DIR / lid
    listing_dir.mkdir(parents=True, exist_ok=True)

    html_file = listing_dir / "page.html"
    html_file.write_text(resp.text, encoding="utf-8")

    soup = BeautifulSoup(resp.text, "html.parser")
    image_paths: list[str] = []
    for i, img_tag in enumerate(soup.find_all("img"), start=1):
        src = img_tag.get("src")
        if not src:
            continue
        if src.startswith("/"):
            src = "https://www.autotrader.com" + src
        try:
            img_resp = requests.get(src, headers=headers, timeout=15)
            img_resp.raise_for_status()
        except Exception:
            continue
        suffix = src.split(".")[-1].split("?")[0]
        img_file = listing_dir / f"image_{i}.{suffix}"
        img_file.write_bytes(img_resp.content)
        image_paths.append(str(img_file))

    meta = {
        "id": listing.get("id"),
        "title": listing.get("title"),
        "url": listing.get("url"),
        "html_file": str(html_file),
        "images": image_paths,
    }
    (listing_dir / "metadata.json").write_text(json.dumps(meta, indent=2))


def fetch_listings(url: str) -> list[dict[str, str]]:
    """Fetch and parse listings from AutoTrader search results."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")
    listings = []
    
    for div in soup.select("div[data-listing-id]"):
        lid = div.get("data-listing-id")
        title = div.get_text(" ", strip=True)[:80]
        listing_url = f"https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId={lid}"
        listings.append({"id": lid, "title": title, "url": listing_url})
    
    return listings


def send_email(cfg: dict, msg: str) -> None:
    mime = MIMEText(msg)
    mime["Subject"] = "New AutoTrader listing"
    mime["From"] = cfg["GMAIL_USER"]
    mime["To"] = cfg["GMAIL_USER"]

    import smtplib

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(cfg["GMAIL_USER"], cfg["GMAIL_APP_PASSWORD"])
        smtp.sendmail(cfg["GMAIL_USER"], [cfg["GMAIL_USER"]], mime.as_string())


def send_sms(cfg: dict, msg: str) -> None:
    client = Client(cfg["TWILIO_SID"], cfg["TWILIO_TOKEN"])
    client.messages.create(body=msg, from_=cfg["TWILIO_FROM"], to=cfg["TWILIO_TO"])


def notify(cfg: dict, listing: dict) -> None:
    msg = f"{listing['title']}\n{listing['url']}"
    try:
        send_email(cfg, msg)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to send email: {exc}")
    try:
        send_sms(cfg, msg)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to send SMS: {exc}")


def main() -> None:
    if "--setup" in sys.argv:
        interactive_setup()
        return

    cfg = load_config()
    seen = load_seen()
    listings = fetch_listings(cfg["SEARCH_URL"])
    new = [l for l in listings if l["id"] not in seen]

    for listing in new:
        notify(cfg, listing)
        seen.add(listing["id"])
        archive_listing(listing)

    save_seen(seen)
    print(f"Processed {len(new)} new listings.")


if __name__ == "__main__":
    main()
