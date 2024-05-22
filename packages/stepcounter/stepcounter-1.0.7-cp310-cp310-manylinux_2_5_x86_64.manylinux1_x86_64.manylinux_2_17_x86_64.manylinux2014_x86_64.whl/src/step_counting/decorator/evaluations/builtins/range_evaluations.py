from ..complexities import (
    ComplexitiesDict,
    constant,
    linear_to_len,
)


range_complexities: ComplexitiesDict = {
    # Dunders
    '__bool__': constant,
    '__contains__': constant,
    '__getitem__': constant,
    '__hash__': constant,
    '__iter__': constant,
    '__len__': constant,
    '__repr__': linear_to_len,
    '__reversed__': constant,
    '__setattr__': constant,
    '__str__': linear_to_len,
    # Comparison
    '__lt__': constant,
    '__le__': constant,
    '__eq__': constant,
    '__ne__': constant,
    '__gt__': constant,
    '__ge__': constant,
    # PyMethodDef
    'count': constant,
    'index': linear_to_len,
}
