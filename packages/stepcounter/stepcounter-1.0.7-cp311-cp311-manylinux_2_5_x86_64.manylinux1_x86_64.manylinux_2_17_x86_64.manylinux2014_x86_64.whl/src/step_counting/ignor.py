from importlib.machinery import BuiltinImporter, FrozenImporter
from typing import Hashable, Optional

IGNORED_OBJECT_METHODS = {
    '__class__',
    '__dir__',
    '__getattribute__',
    '__init__',
    '__new__',
    '__next__',
    '__doc__',
    '__delitem__',  # Performed by the same function as setitem
    '__alloc__',
    '__format__',  # Can be removed after fix in restrict
}

COMPARISON_METHODS = {'__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__ne__'}

IGNORED_R_METHODS = {
    '__radd__',
    '__rand__',
    '__rdivmod__',
    '__rfloordiv__',
    '__rlshift__',
    '__rmod__',
    '__rmul__',
    '__ror__',
    '__rpow__',
    '__rrshift__',
    '__rsub__',
    '__rtruediv__',
    '__rxor__',
}

IGNORED_WIN_METHODS = {
    '_LCMapStringEx',
    '_nt_readlink',
}

IGNORED_R_METHODS = set.union(
    IGNORED_OBJECT_METHODS,
    COMPARISON_METHODS,
    IGNORED_R_METHODS,
    IGNORED_WIN_METHODS,
)

IGNORED_SPECIFICS = {
    (dict, '__iter__'),
}

IGNORED_CLASSES = {BuiltinImporter, FrozenImporter}


def is_ignored(class_: Optional[type], method_name: Optional[str]) -> bool:
    """
    Checks if either class_, method_name or their combination are ignored.

    Parameters
    ----------
    class_ (Optional[type]): class
    method_name (str): name of the method

    Returns
    -------
    bool: Infromation if the class_ or method are ignored.
    """
    return (
        (
            class_
            and (
                class_ in IGNORED_CLASSES
                or not issubclass(class_, Hashable)
                and method_name == '__hash__'
            )
        )
        or method_name in IGNORED_R_METHODS
        or (class_, method_name) in IGNORED_SPECIFICS
    )
