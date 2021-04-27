import types

from . import comparators

def load_validators():
    dict = {}
    for name,item in vars(comparators).items():
        if isinstance(item,types.FunctionType):
            dict[name] = item
    return dict