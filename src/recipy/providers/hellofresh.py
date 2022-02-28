from recipy.providers import base


class HelloFresh(base.BaseProvider):
    provides_for = "www.hellofresh.com"

    def scrape(self):
        if not self.soup:
            self.getSoup()
        print(self.soup.find("h1").text)
