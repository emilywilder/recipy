from recipy.providers import base


class HelloFresh(base.BaseProvider):
    '''Provider for Hello Fresh
    '''
    provides_for = "www.hellofresh.com"

    def scrape(self):
        if not self.soup:
            self.getSoup()
        return {
            "name": self.name
        }

    @property
    def name(self):
        return self.soup.find("h1").text
