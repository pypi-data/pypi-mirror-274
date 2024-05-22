from ..complexities import (
    ComplexitiesDict,
    constant,
    hash_complexity_sec,
    linear_to_len,
    comparison_com,
    linear_to_len_sec,
)

dict_items_complexities: ComplexitiesDict = {
    # Dunders
    '__and__': linear_to_len_sec,
    '__contains__': hash_complexity_sec,
    '__iter__': constant,
    '__len__': constant,
    '__or__': linear_to_len,
    '__repr__': linear_to_len,
    '__reversed__': linear_to_len,
    '__setattr__': constant,
    '__str__': linear_to_len,
    '__sub__': linear_to_len,
    '__xor__': linear_to_len,
    # Comparisons
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    # PyMethodDef
    'isdisjoint': linear_to_len,
    'mapping': constant,
}
