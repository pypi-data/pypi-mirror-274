from ..complexities import (
    ComplexitiesDict,
    comparison_com,
    constant,
)


def slice_size_complexity(args: tuple[slice, ...]) -> int:
    """
    Returns complexity of slicing.

    Parameters
    ----------
    args: function arguments

    Returns
    -------
    int: complexity of slicing
    """
    slice_ = args[0]
    start = slice_.start if slice_.start is not None else 0
    stop = slice_.stop if slice_.stop is not None else 0
    step = slice_.step if slice_.step is not None else 1

    return int((stop - start) // step)


slice_complexities: ComplexitiesDict = {
    # Dunders
    '__repr__': slice_size_complexity,
    '__setattr__': constant,
    '__str__': slice_size_complexity,
    # Comparisons
    '__lt__': comparison_com,
    '__le__': comparison_com,
    '__eq__': comparison_com,
    '__ne__': comparison_com,
    '__gt__': comparison_com,
    '__ge__': comparison_com,
    # PyMethodDef
    'indices': constant,
}
