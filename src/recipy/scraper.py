from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from recipy.providers import utils


class Scraper(object):
    def __init__(self, url, schema):
        self.url = url
        self.schema = schema
        self.soup = None
        self.provider = None
        self.data = {}

    def _getSoup(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def _getProvider(self):
        hostname = urlparse(self.url).hostname
        self.provider = utils.get_provider(hostname)(self.soup)

    def scrape(self):
        if not self.soup:
            self._getSoup()
        if not self.provider:
            self._getProvider()

        for _attr in self.schema.attrs:
            self.data[_attr] = getattr(self.provider, _attr)
