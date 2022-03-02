from recipy.providers import base


class HelloFresh(base.BaseProvider):
    '''Provider for Hello Fresh
    '''
    provides_for = "www.hellofresh.com"

    @property
    def name(self):
        return self.soup.find("h1").get_text().strip()
