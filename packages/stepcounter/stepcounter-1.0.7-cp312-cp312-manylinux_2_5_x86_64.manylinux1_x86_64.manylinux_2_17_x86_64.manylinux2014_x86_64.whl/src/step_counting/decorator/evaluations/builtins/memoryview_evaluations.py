
from ..complexities import (
    ComplexitiesDict,
    comparison_com,
    constant,
    linear_to_len,
)


memoryview_complexities: ComplexitiesDict = {
    # Dunders
    '__enter__': constant,
    '__exit__': constant,
    '__getitem__': constant,
    '__iter__': constant,
    '__len__': constant,
    '__repr__': constant,
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
    'c_contiguous': constant,
    'cast': constant,
    'contiguous': constant,
    'f_contiguous': constant,
    'format': constant,
    'hex': linear_to_len,
    'itemsize': constant,
    'nbytes': constant,
    'ndim': constant,
    'obj': constant,
    'readonly': constant,
    'release': constant,
    'shape': constant,
    'strides': constant,
    'suboffsets': constant,
    'tobytes': linear_to_len,
    'tolist': linear_to_len,
    'toreadonly': constant,
}
