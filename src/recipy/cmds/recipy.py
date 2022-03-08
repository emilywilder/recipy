import argparse
import logging
import sys

from recipy import schemas
from recipy import scraper
from recipy import exports

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Scrape recipe contents into a YAML file')
    parser.add_argument('url', help="URL of recipe")

    # TODO: add schema selection
    # TODO: add output format selection

    args = parser.parse_args()

    try:
        # get schema and scraper
        schema = schemas.PaprikaSchema()
        _scraper = scraper.Scraper(args.url, schema)

        # perform scraping of website
        _scraper.scrape()

        # validate data with schema
        schema.validate(_scraper.data)

        # save data in yaml format
        filename = "{0}.yml".format(
            _scraper.data.get("name")
        )
        with open(filename, 'w') as f:
            exports.yaml.dump(_scraper.data, f, allow_unicode=True)

        logging.info(_scraper.data)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
