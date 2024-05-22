from ..complexities import (
    ComplexitiesDict,
    constant,
    linear_to_len,
    comparison_com,
)


dict_values_complexities: ComplexitiesDict = {
    # Dunders
    '__hash__': linear_to_len,
    '__iter__': constant,
    '__len__': constant,
    '__repr__': linear_to_len,
    '__reversed__': linear_to_len,
    '__setattr__': constant,
    '__str__': linear_to_len,
    # Comparisons
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    # PyMethodDef
    'isdisjoint': linear_to_len,
    'mapping': constant,
}
