import recipy.schemas


class TestHelloFresh():
    '''tests for HelloFreshSchema'''
    def test_spec(self):
        hf = recipy.schemas.HelloFreshSchema()
        for attr in recipy.schemas.HelloFreshSchema.specification:
            assert attr in hf.schema
