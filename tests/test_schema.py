import pytest
import schema

import recipy.schemas


def make_schema_data(_schema: schema.Schema) -> dict:
    """create skeleton data according to given schema"""
    data = {}
    for (k, v) in _schema.schema.items():
        if issubclass(v, str):
            data[k] = ''
        elif issubclass(v, list):
            data[k] = []
        else:
            raise Exception("Can't create data for unknown type: {0}".format(v))
    return data


class TestPaprika:
    """tests for PaprikaSchema"""
    def test_spec(self):
        s = recipy.schemas.PaprikaSchema()
        for attr in recipy.schemas.PaprikaSchema.specification:
            assert attr in s.schema

    def test_attrs_method(self):
        s = recipy.schemas.PaprikaSchema()
        assert s.attrs == s.schema

    @pytest.mark.parametrize("attr, test", [("name", "Emily"), ("prep_time", "x minutes")])
    def test_attr(self, attr, test):
        spec = recipy.schemas.PaprikaSchema.specification.get(attr)
        assert schema.Schema(spec).validate(test)

    def test_wrong_data_type(self):
        s = recipy.schemas.PaprikaSchema()
        data = make_schema_data(s)
        data['name'] = 1
        with pytest.raises(schema.SchemaError):
            s.validate(data)

    def test_wrong_key_present(self):
        s = recipy.schemas.PaprikaSchema()
        data = make_schema_data(s)
        data['notSupposedToBeHere'] = True
        with pytest.raises(schema.SchemaWrongKeyError):
            s.validate(data)
