import argparse
import sys
import logging
from urllib.parse import urlparse
from recipy.providers import base


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    args = parser.parse_args()

    hostname = urlparse(args.url).hostname
    try:
        providerClass = base.BaseProvider.getProvider(hostname)
        provider = providerClass(args.url)
        provider.scrape()
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
