import requests
from bs4 import BeautifulSoup


class BaseProvider(object):
    def __init__(self, url):
        self.url = url
        self.soup = None

    def scrape(self):
        raise NotImplementedError("submodule did not implement the scrape method")

    def getSoup(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')
