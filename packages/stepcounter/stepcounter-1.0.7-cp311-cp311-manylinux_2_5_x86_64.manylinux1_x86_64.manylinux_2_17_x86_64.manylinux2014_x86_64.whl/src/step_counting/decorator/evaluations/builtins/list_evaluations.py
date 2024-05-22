from typing import Any

from ..complexities import (
    ComplexitiesDict,
    constant,
    linear_to_len,
    comparison_com,
    linear_to_len_sec,
    linearithmic_to_len,
    comparison_com,
    sequence_mul_complexity,
)


def list_insert_complexity(args: tuple[list[Any], int]) -> int:
    """
    Returns complexity of list insert.

    Parameters
    ----------
    args: function arguments

    Returns
    -------
    int: complexity of list insert
    """
    list_ = args[0]
    index = args[1]
    return len(list_) - index + 1


def list_pop_complexity(args: tuple[list[Any], int]) -> int:
    """
    Returns complexity of list pop.

    Parameters
    ----------
    args: function arguments

    Returns
    -------
    int: complexity of list pop
    """
    # In this case, pop is used without a second argument
    # therefore we are popping from the end of the list
    # making the time complexity constant.
    if len(args) < 2:
        return 1

    list_ = args[0]
    index = args[1]
    return len(list_) - index


def list_getitem_complexity(args: tuple[list[Any], int]) -> int:
    """
    Returns complexity of list getitem.

    Parameters
    ----------
    args: function arguments

    Returns
    -------
    int: complexity of list getitem
    """
    elem = args[1]
    if isinstance(elem, slice):
        return (elem.stop - elem.start) // elem.step
    return 1


list_complexities: ComplexitiesDict = {
    # Dunders
    '__add__': linear_to_len_sec,
    '__class_getitem__': constant,
    '__contains__': linear_to_len,
    '__getitem__': list_getitem_complexity,
    '__iadd__': linear_to_len_sec,
    '__imul__': linear_to_len,
    '__iter__': constant,
    '__len__': constant,
    '__mul__': sequence_mul_complexity,
    '__repr__': linear_to_len,
    '__reversed__': linear_to_len,
    '__setattr__': constant,
    '__setitem__': constant,
    '__str__': linear_to_len,
    # Comparisons
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    # PyMethodDef
    'append': constant,
    'clear': linear_to_len,
    'copy': linear_to_len,
    'count': linear_to_len,
    'extend': linear_to_len_sec,
    'index': linear_to_len,
    'insert': list_insert_complexity,
    'pop': list_pop_complexity,
    'remove': linear_to_len,
    'reverse': linear_to_len,
    'sort': linearithmic_to_len,
}
