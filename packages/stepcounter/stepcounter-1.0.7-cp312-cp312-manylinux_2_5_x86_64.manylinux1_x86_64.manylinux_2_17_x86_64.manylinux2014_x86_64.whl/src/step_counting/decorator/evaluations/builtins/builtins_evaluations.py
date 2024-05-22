from ..complexities import ComplexitiesDict, constant, linear_to_len

builtins_complexities: ComplexitiesDict = {
    'print': constant,
    'sum': linear_to_len,
    'enumerate': linear_to_len,
    'open': constant,
}
