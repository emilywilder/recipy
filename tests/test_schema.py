import pytest
import schema

import recipy.schemas


class TestPaprika():
    '''tests for PaprikaSchema'''
    def test_spec(self):
        s = recipy.schemas.PaprikaSchema()
        for attr in recipy.schemas.PaprikaSchema.specification:
            assert attr in s.schema

    def test_attrs(self):
        s = recipy.schemas.PaprikaSchema()
        assert s.attrs == s.schema

    def test_good_data(self):
        s = recipy.schemas.PaprikaSchema()
        data = {"name": "emily"}
        assert s.validate(data)

    def test_bad_data_value(self):
        s = recipy.schemas.PaprikaSchema()
        data = {"name": 1}
        with pytest.raises(schema.SchemaError):
            s.validate(data)

    def test_bad_data_key(self):
        s = recipy.schemas.PaprikaSchema()
        data = {"schemaTest": True}
        with pytest.raises(schema.SchemaMissingKeyError):
            s.validate(data)