from recipy.providers import base


class HelloFresh(base.BaseProvider):
    """Provider for Hello Fresh
    """
    provides_for = "www.hellofresh.com"

    @property
    def name(self) -> str:
        h1 = self.soup.find("h1")
        h4 = h1.find_next_sibling("h4")
        return " ".join([
            h1.get_text().strip(),
            h4.get_text().strip()
        ])

    @property
    def servings(self) -> str:
        tag = self.soup.select_one("[data-test-id='serving-amount-container']")
        divs = tag.find_all("div")
        return "{0} to {1} servings".format(
            divs[2].get_text().strip(),
            divs[3].get_text().strip()
        )

    @property
    def prep_time(self) -> str:
        tag = self.soup.select_one("[data-translation-id='recipe-detail.cooking-time']")
        return tag.find_parent().find_next_sibling().get_text().strip()
