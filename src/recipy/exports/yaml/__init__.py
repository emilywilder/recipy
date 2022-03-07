from yaml import *


class Folded(str):
    pass


class Literal(str):
    pass


def folded_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')


def literal_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


add_representer(Folded, folded_representer)
add_representer(Literal, literal_representer)
