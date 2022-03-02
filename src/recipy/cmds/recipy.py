import argparse
import sys
import logging
from urllib.parse import urlparse
from recipy.providers.utils import get_provider

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    args = parser.parse_args()

    try:
        logging.info(scraper(args.url))
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)


def scraper(url):
    import requests
    from bs4 import BeautifulSoup

    hostname = urlparse(url).hostname

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    providerClass = get_provider(hostname)
    provider = providerClass(soup)
    return {"name": provider.name}
