from typing import Any

from ..complexities import (
    ComplexitiesDict,
    constant,
    hash_complexity_sec,
    linear_to_len,
    comparison_com,
    linear_to_len_sec,
    linear_to_len_sum,
)


def min_len_complexity(args: tuple[Any, ...]) -> int:
    """
    Returns min of two lenghts.

    Parameters
    ----------
    args: function arguments

    Returns
    -------
    int: min of two lenghts
    """
    set_one = args[0]
    set_two = args[1]
    return min(len(set_one), len(set_two))


set_complexities: ComplexitiesDict = {
    # Dunders
    '__and__': linear_to_len_sec,
    '__class_getitem__': constant,
    '__contains__': hash_complexity_sec,
    '__iand__': linear_to_len_sec,
    '__ior__': linear_to_len_sum,
    '__isub__': linear_to_len_sec,
    '__iter__': constant,
    '__ixor__': linear_to_len_sum,
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
    'add': constant,
    'clear': linear_to_len,
    'copy': linear_to_len,
    'difference': linear_to_len_sum,
    'difference_update': linear_to_len_sum,
    'discard': constant,
    'intersection': min_len_complexity,
    'intersection_update': min_len_complexity,
    'isdisjoint': min_len_complexity,
    'issubset': min_len_complexity,
    'issuperset': min_len_complexity,
    'pop': constant,
    'remove': constant,
    'symmetric_difference': linear_to_len_sum,
    'symmetric_difference_update': linear_to_len_sum,
    'union': linear_to_len_sum,
    'update': linear_to_len_sum,
}
