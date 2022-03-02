import argparse
import sys
import logging
import yaml

from recipy.scraper import Scraper
from recipy import schemas

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    # TODO: add schema selection
    # TODO: add output format selection

    args = parser.parse_args()

    try:
        # get schema and scraper
        schema = schemas.HelloFreshSchema()
        scraper = Scraper(args.url, schema)

        # perform scraping of website
        scraper.scrape()

        # validate data with schema
        schema.validate(scraper.data)

        # save data in yaml format
        filename = "{0}.yml".format(
            scraper.data.get("name")
        )
        with open(filename, 'w') as f:
            yaml.dump(scraper.data, f)

        logging.info(scraper.data)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
