import tldextract

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
        tag = self.soup.find('div', attrs={'data-test-id': 'serving-amount-container'})
        divs = tag.find_all("div")
        return "{0} to {1} servings".format(
            divs[2].get_text().strip(),
            divs[3].get_text().strip()
        )

    @property
    def source(self) -> str:
        return tldextract.extract(self.source_url).registered_domain

    @property
    def source_url(self) -> str:
        return self.soup.find('head').find("link", rel="canonical").get("href")

    @property
    def prep_time(self) -> str:
        tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.cooking-time'})
        return tag.find_parent().find_next_sibling().get_text().strip()

    @property
    def cook_time(self) -> str:
        tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.preparation-time'})
        return tag.find_parent().find_next_sibling().get_text().strip()

    @property
    def categories(self) -> list:
        return [self.source]

    @property
    def nutritional_info(self) -> str:
        container_div = self.soup.find('div', attrs={'data-test-id': 'recipeDetailFragment.nutrition-values'})
        # div containing relevant divs to iterate
        tag = container_div.find_all('div', recursive=False)[-1].find_next('div').find_all('div', recursive=False)
        # use stripped_strings to handle case where newlines are used
        # discard last div contents, as this is just disclaimer details
        details = list(' '.join(x.stripped_strings) for x in tag)[:-1]
        return "\n".join(details)
