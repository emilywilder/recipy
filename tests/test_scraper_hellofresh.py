import pytest
import requests
import base64

from recipy import schemas
from recipy.scraper import Scraper

HF_TEST_URL = "https://www.hellofresh.com/testrecipe"


def b64encode(data):
    return base64.b64encode(data).decode('utf8')


def get_sample_img_data():
    with open('tests/sample.jpeg', 'rb') as f:
        return f.read()


# FIXME: when this breaks it breaks all tests in the parametrization
class MockResponse:
    def __init__(self, resource):
        if resource == "https://www.hellofresh.com/testrecipe":
            with open("tests/test_hellofresh.html", 'r') as f:
                self.text = f.read()
        elif resource == "tests/sample.jpeg":
            self.content = get_sample_img_data()
        else:
            raise Exception("can't handle resource {0}".format(resource))


@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(args[0])

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.mark.parametrize("attr, expected",
                         [("name", "Recipy with additional awesomeness"),
                          ("servings", "3 to 6 servings"),
                          ("source", "hellofresh.com"),
                          ("source_url", "https://www.hellofresh.com/recipes/recipy-with-extra-awesome"),
                          ("prep_time", "22 minutes"),
                          ("cook_time", "55 minutes"),
                          ("categories", ["hellofresh.com"]),
                          ("nutritional_info", '\n'.join([
                              "Calories 1000 kcal", "Fat 5 g", "Saturated Fat 10 g", "Carbohydrate 15 g", "Sugar 20 g",
                              "Dietary Fiber 25 g", "Protein 30 g", "Cholesterol 35 mg", "Sodium 40 mg"])),
                          ("difficulty", 'Über hard'),
                          ("notes", 'Recipe read more'),
                          ("photo", b64encode(get_sample_img_data()))
                          ])
def test_get_attrs(attr, expected, mock_response):
    schema = schemas.PaprikaSchema()

    scraper = Scraper(HF_TEST_URL, schema)
    scraper.scrape()
    assert scraper.data.get(attr) == expected
