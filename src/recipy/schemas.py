from schema import Schema


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
    """
    specification = {
        "name": str,
        "servings": str,
        "source": str,
        "source_url": str,
        "prep_time": str
    }
