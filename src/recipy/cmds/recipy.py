import argparse
import sys
import logging
from recipy.scraper import Scraper

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    args = parser.parse_args()

    try:
        scraper = Scraper(args.url)
        scraper.scrape()
        logging.info(scraper.data)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
