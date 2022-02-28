import argparse
import sys
import logging
from urllib.parse import urlparse
from recipy.providers.base import BaseProvider


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    args = parser.parse_args()

    hostname = urlparse(args.url).hostname
    try:
        provider = BaseProvider.getProvider(hostname)
        print("TODO: use the provider {0} to scrape {1}".format(provider, args.url))
    except Exception as e:
        logging.error(e.message)
        sys.exit(1)