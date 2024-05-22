from ..complexities import (
    ComplexitiesDict,
    constant,
    hash_complexity,
    linear_to_len,
    comparison_com,
    sequence_mul_complexity,
)


tuple_complexities: ComplexitiesDict = {
    # Dunders
    '__add__': constant,
    '__class_getitem__': constant,
    '__contains__': linear_to_len,
    '__getitem__': constant,
    '__hash__': hash_complexity,
    '__iter__': constant,
    '__len__': constant,
    '__mul__': sequence_mul_complexity,
    '__repr__': linear_to_len,
    '__setattr__': constant,
    '__str__': linear_to_len,
    # Comparisons
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    # PyMethodDef
    'count': linear_to_len,
    'index': linear_to_len,
}
