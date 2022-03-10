import tldextract
import base64
import requests
import re

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
        # only use first number, as this represents the ingredients given
        return "{0} servings".format(divs[2].get_text().strip())

    @property
    def source(self) -> str:
        return tldextract.extract(self.source_url).registered_domain

    @property
    def source_url(self) -> str:
        return self.soup.find('head').find("link", rel="canonical").get("href")

    @property
    def prep_time(self) -> str:
        # hellofresh.com uses recipe-detail.cooking-time for prep time
        tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.cooking-time'})
        return tag.find_parent().find_next_sibling().get_text().strip()

    @property
    def total_time(self) -> str:
        # hellofresh.com uses recipe-detail.preparation-time for cook time
        tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.preparation-time'})
        return tag.find_parent().find_next_sibling().get_text().strip()

    @staticmethod
    def _get_minutes(time):
        return int(time.split()[0])

    @property
    def cook_time(self) -> str:
        # assumes total_time and prep_time only in minutes
        _cook_time = self._get_minutes(self.total_time) - self._get_minutes(self.prep_time)
        return "{0} minutes".format(_cook_time)

    @property
    def categories(self) -> list:
        return [self.__class__.__name__] + self.tags

    @property
    def nutritional_info(self) -> str:
        container_div = self.soup.find('div', attrs={'data-test-id': 'recipeDetailFragment.nutrition-values'})
        # div containing relevant divs to iterate
        tag = container_div.find_all('div', recursive=False)[-1].find_next('div').find_all('div', recursive=False)
        # use stripped_strings to handle case where newlines are used
        # discard last div contents, as this is just disclaimer details
        details = list(' '.join(x.stripped_strings) for x in tag)[:-1]
        return Literal("\n".join(details))

    @property
    def difficulty(self) -> str:
        nv_tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.cooking-difficulty'})
        return nv_tag.find_next('span').get_text().strip()

    @property
    def description(self) -> Literal:
        r_tag = self.soup.find('span', attrs={'data-translation-id': 'recipe-detail.read-more'})
        _description = r_tag.find_parent('div').p.get_text().strip()
        _tags = "Tags: {0}".format(", ".join(self.tags))
        _allergens = "Allergens: {0}".format(", ".join(self.allergens))

        return Literal("\n\n".join([_description, _tags, _allergens]))

    @property
    def photo(self) -> str:
        img_src = self.soup.find('img', attrs={'alt': self._name_h1()}).attrs.get('src')
        r = requests.get(img_src)
        return base64.b64encode(r.content).decode('utf-8')

    @property
    def ingredients(self) -> Literal:
        # get container of in and out of box divs
        container = self.soup.find('div', attrs={'data-test-id': 'recipeDetailFragment.ingredients'})
        # contains ingredients delivered in the box
        box = container.find_all('div', recursive=False)[-2].find('div')
        box_contents = box.find_all('div', recursive=False)
        # contains ingredients not delivered in the box
        pantry = container.find_all('div', recursive=False)[-1].find('div')
        pantry_contents = pantry.div.find_all('div', recursive=False)

        # pass box and pantry divs to a method to get formatted text of contents
        contents = list(map(self.get_ingredient_text, box_contents + pantry_contents))
        return Literal('\n'.join(contents))

    @staticmethod
    def get_ingredient_text(div):
        # get the ingredient text
        text = ' '.join([x.get_text().strip() for x in div.find_all('p')]).strip()

        # if the ingredient contains allergens, format ingredient text to include them
        contains = div.find('span', attrs={"data-translation-id": "recipe-detail.contains"})
        if contains:
            contents = contains.find_parent('span').find_next_sibling('span').get_text().strip()
            text = "{0} ({1} {2})".format(text, contains.text.strip(), contents)

        return text

    @property
    def directions(self) -> Literal:
        # get all divs matching instruction steps
        s = re.compile('recipeDetailFragment.instructions.step-[0-9]')
        divs = self.soup.find_all('div', attrs={'data-test-id': s})
        # Each instruction div has one <p> giving the instructional text.

        return Literal("\n\n".join(list(map(self.format_direction, divs))))

    @staticmethod
    def format_direction(div) -> str:
        # get direction step, used in html structure
        step = div.attrs.get('data-test-id').split('-')[-1]
        # get direction number, used in direction text
        instruction_num = div.find("div",
                                   attrs={"data-test-id": "recipeDetailFragment.instructions.step-image-" + step}
                                   ).get_text().strip()
        # get direction text from <p>
        text = div.find("p").get_text().strip()
        # replace the first • with the direction number, then split on • to get a list of sub-directions
        directions = text.replace("•", "{0}. ".format(instruction_num), 1).split('•')
        # remove existing newlines from each sub-direction and join all sub-directions by newlines
        return '\n'.join([x.replace('\n', ' ').strip() for x in directions])

    @property
    def notes(self) -> Literal:
        _utensils = "Utensils: {0}".format(", ".join(self.utensils))
        return Literal('\n\n'.join([_utensils, self._stamp()]))

    @staticmethod
    def _filter_items_from_tag(tag) -> list:
        return list(filter(lambda x: x != '•', tag.stripped_strings))

    @property
    def allergens(self) -> list:
        tag = self.soup.find('span', attrs={"data-translation-id": "recipe-detail.allergens"})
        allergens = tag.find_parent('span').find_next_sibling()
        return self._filter_items_from_tag(allergens)

    @property
    def tags(self) -> list:
        tag = self.soup.find('span', attrs={"data-translation-id": "recipe-detail.tags"})
        tags = tag.find_parent('span').find_next_sibling()
        return self._filter_items_from_tag(tags)

    @property
    def utensils(self) -> list:
        tag = self.soup.find('div', attrs={"data-test-id": "utensil-desktop-title"})
        utensils_tag = tag.find_parent('div').find_parent('div').find_next_sibling('div')
        return self._filter_items_from_tag(utensils_tag)
