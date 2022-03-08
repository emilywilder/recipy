import tldextract
import base64
import requests

from recipy.providers import base
from recipy.exports.yaml import Literal


class HelloFresh(base.BaseProvider):
    """Provider for Hello Fresh
    """
    provides_for = "www.hellofresh.com"

    def _name_h1(self) -> str:
        return self.soup.find("h1").get_text().strip()

    def _name_h4(self) -> str:
        return self.soup.find("h4").get_text().strip()

    @property
    def name(self) -> str:
        return " ".join([
            self._name_h1(),
            self._name_h4()
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

    @property
    def difficulty(self) -> str:
        nv_tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.cooking-difficulty'})
        return nv_tag.find_next('span').get_text().strip()

    @property
    def notes(self) -> Literal:
        r_tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.read-more'})
        return Literal(r_tag.find_parent('div').p.get_text().strip())

    @property
    def photo(self) -> str:
        img_src = self.soup.find('img', attrs={'alt': self._name_h1()}).attrs.get('src')
        r = requests.get(img_src)
        return base64.b64encode(r.content).decode('utf-8')
