import pytest
import requests

from recipy import schemas
from recipy.scraper import Scraper

HF_TEST_URL = "https://www.hellofresh.com/testrecipe"


class MockResponse:
    with open("tests/test_hellofresh.html", 'r') as f:
        text = f.read()


@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.mark.parametrize("attr, expected",
                         [("name", "Recipy with additional awesomeness"),
                          ("servings", "3 to 6 servings"),
                          ("prep_time", "22 minutes")])
def test_get_attrs(attr, expected, mock_response):
    schema = schemas.PaprikaSchema()

    scraper = Scraper(HF_TEST_URL, schema)
    scraper.scrape()
    assert scraper.data.get(attr) == expected
