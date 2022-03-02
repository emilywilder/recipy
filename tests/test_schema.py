import pytest
import schema

import recipy.schemas


class TestHelloFresh():
    '''tests for HelloFreshSchema'''
    def test_spec(self):
        hf = recipy.schemas.HelloFreshSchema()
        for attr in recipy.schemas.HelloFreshSchema.specification:
            assert attr in hf.schema

    def test_attrs(self):
        hf = recipy.schemas.HelloFreshSchema()
        assert hf.attrs == hf.schema

    def test_good_data(self):
        hf = recipy.schemas.HelloFreshSchema()
        data = {"name": "emily"}
        assert hf.validate(data)

    def test_bad_data_value(self):
        hf = recipy.schemas.HelloFreshSchema()
        data = {"name": 1}
        with pytest.raises(schema.SchemaError):
            hf.validate(data)

    def test_bad_data_key(self):
        hf = recipy.schemas.HelloFreshSchema()
        data = {"schemaTest": True}
        with pytest.raises(schema.SchemaMissingKeyError):
            hf.validate(data)
