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

    hostname = urlparse(args.url).hostname
    try:
        providerClass = get_provider(hostname)
        provider = providerClass(args.url)
        result = provider.scrape()
        logging.info(result)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
