from ..complexities import ComplexitiesDict, constant


complex_complexities: ComplexitiesDict = {
    # Dunders
    '__abs__': constant,
    '__add__': constant,
    '__bool__': constant,
    '__hash__': constant,
    '__mul__': constant,
    '__neg__': constant,
    '__pos__': constant,
    '__pow__': constant,
    '__repr__': constant,
    '__setattr__': constant,
    '__str__': constant,
    '__sub__': constant,
    '__truediv__': constant,
    # Comparisons
    '__eq__': constant,
    '__ne__': constant,
    # PyMethodDef
    'conjugate': constant,
    'imag': constant,
    'real': constant,
}
