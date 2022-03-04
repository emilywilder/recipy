class BaseProvider(object):
    provides_for = ""

    def __init__(self, soup):
        self.soup = soup
