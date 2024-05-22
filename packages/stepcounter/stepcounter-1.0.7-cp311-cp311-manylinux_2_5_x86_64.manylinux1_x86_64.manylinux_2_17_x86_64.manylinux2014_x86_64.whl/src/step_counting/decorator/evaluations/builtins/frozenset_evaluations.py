
from ..complexities import (
    ComplexitiesDict,
    comparison_com,
    constant,
    linear_to_len,
    linear_to_len_sec,
    linear_to_len_sum,
)


frozenset_complexities: ComplexitiesDict = {
    # Dunders
    '__and__': linear_to_len_sec,
    '__class_getitem__': constant,
    '__contains__': constant,
    '__hash__': linear_to_len,
    '__iter__': constant,
    '__len__': constant,
    '__or__': linear_to_len_sum,
    '__repr__': linear_to_len,
    '__setattr__': constant,
    '__str__': linear_to_len,
    '__sub__': linear_to_len_sec,
    '__xor__': linear_to_len_sum,
    # Comparisons
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    # PyMethodDef
    'copy': constant,
    'difference': linear_to_len,
    'intersection': linear_to_len,
    'isdisjoint': linear_to_len,
    'issubset': linear_to_len,
    'issuperset': linear_to_len,
    'symmetric_difference': linear_to_len,
    'union': linear_to_len,
}
