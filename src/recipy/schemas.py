from schema import Schema
from recipy.exports import yaml


class BaseSchema(Schema):
    specification = {}

    def __init__(self, schema=None, error=None, **kwargs):
        if not schema:
            schema = self.specification
        super().__init__(schema, error, **kwargs)

    @property
    def attrs(self):
        return self.schema


class PaprikaSchema(BaseSchema):
    """Provides a class to describe the structure and validation of Paprika imports.

    As per their specification (https://www.paprikaapp.com/help/mac/#importrecipes):

    name: My Tasty Recipe
    servings: 4-6 servings
    source: Food Network
    source_url: http://www.google.com
    prep_time: 10 min
    cook_time: 30 min
    on_favorites: yes
    categories: [Dinner, Holiday]
    nutritional_info: 500 calories
    difficulty: Easy
    rating: 5
    notes: |
      This is delicious!!!
    photo: (base-64 encoded image)
    ingredients: |
      1/2 lb meat
      1/2 lb vegetables
      salt
      pepper
      2 tbsp olive oil
      4 cups flour
    directions: |
      Mix things together.
      Eat.
      Tasty.
      Yum yum yum.
    """
    specification = {
        "name": str,
        "servings": str,
        "source": str,
        "source_url": str,
        "prep_time": str,
        "cook_time": str,
        # "on_favorites": str,
        "categories": list,
        "nutritional_info": str,
        "difficulty": str,
        # "rating": int,
        "description": yaml.Literal,
        "photo": str,
        "ingredients": yaml.Literal,
        "directions": yaml.Literal,
    }

