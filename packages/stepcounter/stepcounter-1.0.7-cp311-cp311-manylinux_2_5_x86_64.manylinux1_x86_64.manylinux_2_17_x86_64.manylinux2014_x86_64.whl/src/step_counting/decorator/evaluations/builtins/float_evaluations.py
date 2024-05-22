from ..complexities import ComplexitiesDict, constant, logarithmic_to_sec


float_complexities: ComplexitiesDict = {
    # Dunders
    '__abs__': constant,
    '__add__': constant,
    '__bool__': constant,
    '__ceil__': constant,
    '__divmod__': constant,
    '__float__': constant,
    '__floor__': constant,
    '__floordiv__': constant,
    '__getformat__': constant,
    '__hash__': constant,
    '__int__': constant,
    '__mod__': constant,
    '__mul__': constant,
    '__neg__': constant,
    '__pos__': constant,
    '__pow__': constant,
    '__repr__': constant,
    '__round__': constant,
    '__setattr__': constant,
    '__str__': constant,
    '__sub__': constant,
    '__truediv__': constant,
    '__trunc__': constant,
    # Comparisons
    '__lt__': constant,
    '__le__': constant,
    '__eq__': constant,
    '__ne__': constant,
    '__gt__': constant,
    '__ge__': constant,
    # PyMethodDef
    'as_integer_ratio': constant,
    'conjugate': constant,
    'fromhex': constant,
    'hex': constant,
    'imag': constant,
    'is_integer': constant,
    'real': constant,
}
