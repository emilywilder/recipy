from recipy.providers import base


class HelloFresh(base.BaseProvider):
    '''Provider for Hello Fresh
    '''
    provides_for = "www.hellofresh.com"

    @property
    def name(self):
        return self.soup.find("h1").get_text().strip()

    @property
    def prep_time(self):
        tag = self.soup.select_one("[data-translation-id='recipe-detail.cooking-time']")
        return tag.parent.next_sibling.text.strip()
