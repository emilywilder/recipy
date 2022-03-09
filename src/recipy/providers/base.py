from datetime import date

import recipy


class BaseProvider(object):
    provides_for = ""

    def __init__(self, soup) -> None:
        self.soup = soup

    @staticmethod
    def _stamp() -> str:
        return "Obtained by {name}-{version} on {date}".format(
            name=recipy.__name__,
            version=recipy.VERSION,
            date=date.today().strftime("%B %d, %Y"),
        )
