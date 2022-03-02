import pytest
import requests

from recipy import schemas
from recipy.scraper import Scraper


class MockHelloFreshResponse:
    with open("tests/test_hellofresh.html", 'r') as f:
        text = f.read()


def test_get_text(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockHelloFreshResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    schema = schemas.PaprikaSchema()
    hf_test_url = "https://www.hellofresh.com/testrecipe"
    scraper = Scraper(hf_test_url, schema)
    scraper.scrape()
    assert scraper.data.get("name") == "Recipy"
