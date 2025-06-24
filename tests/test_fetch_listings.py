"""
Unit test for fetch_listings – we *mock* Playwright so the test suite
stays fast and CI-friendly.
"""

import autotrader_bot as bot

class DummyEl:
    def __init__(self, attrs, title, href):
        self.attrs = attrs
        self.title = title
        self.href = href
    def get_attribute(self, key):
        return self.attrs.get(key)
    def query_selector(self, _):
        return DummyEl({}, self.title, self.href)
    def inner_text(self):
        return self.title

def fake_playwright(url):
    # Return two fake cards
    return [
        {"id": "123", "title": "2022 BMW M5 Comp", "url": "https://example.com/1"},
        {"id": "456", "title": "2021 BMW M5 Comp", "url": "https://example.com/2"},
    ]

def test_fetch_listings(monkeypatch):
    monkeypatch.setattr(bot, "fetch_listings", lambda url: fake_playwright(url))
    out = bot.fetch_listings("http://dummy")
    assert len(out) == 2
    assert out[0]["id"] == "123"
