import sys
import types
from pathlib import Path

import pytest

# Stub external modules that autotrader_bot depends on but are not installed in
# the test environment.
sys.modules.setdefault("dotenv", types.SimpleNamespace(load_dotenv=lambda: None))
sys.modules.setdefault("twilio", types.ModuleType("twilio"))
sys.modules.setdefault("twilio.rest", types.ModuleType("twilio.rest"))
sys.modules["twilio.rest"].Client = object
sys.modules.setdefault("requests", types.ModuleType("requests"))

# Ensure the project root is on sys.path so autotrader_bot can be imported when
# tests are run directly.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

class _DummyDiv:
    def __init__(self, lid: str, text: str) -> None:
        self._id = lid
        self._text = text

    def get(self, attr: str) -> str | None:
        return self._id if attr == "data-listing-id" else None

    def get_text(self, sep: str = " ", strip: bool = False) -> str:
        text = " ".join(self._text.split())
        return text.strip() if strip else text


class _DummySoup:
    def __init__(self, html: str, parser: str) -> None:  # noqa: D401
        # Minimal parser that finds div elements with data-listing-id.
        import re

        pattern = re.compile(r'<div[^>]*data-listing-id="(\d+)"[^>]*>(.*?)</div>', re.S)
        self._matches = [
            _DummyDiv(lid, re.sub("<.*?>", "", content)) for lid, content in pattern.findall(html)
        ]

    def select(self, selector: str):
        if selector == "div[data-listing-id]":
            return self._matches
        return []


sys.modules.setdefault("bs4", types.ModuleType("bs4"))
sys.modules["bs4"].BeautifulSoup = _DummySoup

import autotrader_bot
fetch_listings = autotrader_bot.fetch_listings

SAMPLE_HTML = """
<html>
  <body>
    <div data-listing-id="12345">
       <h2>Sample Car</h2>
    </div>
    <div data-listing-id="67890">
       <h2>Another Car</h2>
    </div>
  </body>
</html>
"""

class DummyResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self):
        pass


def dummy_get(url: str, timeout: int = 15, headers: dict | None = None):
    return DummyResponse(SAMPLE_HTML)


def test_fetch_listings(monkeypatch):
    monkeypatch.setattr("requests.get", dummy_get, raising=False)
    listings = fetch_listings("http://example.com")
    assert listings == [
        {
            "id": "12345",
            "title": "Sample Car",
            "url": "https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=12345",
        },
        {
            "id": "67890",
            "title": "Another Car",
            "url": "https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=67890",
        },
    ]

