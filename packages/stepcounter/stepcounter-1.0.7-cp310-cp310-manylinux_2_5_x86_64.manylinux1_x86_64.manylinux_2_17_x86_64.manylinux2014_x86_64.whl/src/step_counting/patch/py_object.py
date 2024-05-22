from typing import Optional
from collections import deque

from ctypes import (
    c_uint,
    c_int,
    c_char_p,
    c_void_p,
    c_ulong,
    c_ubyte,
    py_object,
    c_ssize_t,
    CFUNCTYPE,
    POINTER,
    Structure,
)


from ..non_builtin_types import (
    dict_items_type,
    dict_keys_type,
    dict_values_type,
)


class PyObject(Structure):
    pass


class PyTypeObject(Structure):
    pass


# Common function types
unary = (py_object, py_object)
binary = (py_object, py_object, py_object)
ternary = (py_object, py_object, py_object, py_object)
ssize_unary = (c_ssize_t, py_object)
index_f = (py_object, py_object, c_ssize_t)
iassign_f = (c_int, py_object, c_ssize_t, py_object)
init_f = (c_int, py_object, py_object, c_void_p)
int_ternary = (c_int, py_object, py_object, py_object)
ssize_ternary = (c_ssize_t, py_object, py_object, py_object)

# Additional types for type object structure
destructor_type = (c_void_p, py_object)
tp_richcompare_type = (py_object, py_object, py_object, c_int)
tp_getattr_type = (py_object, py_object, c_char_p)
tp_setattr_type = (c_int, py_object, c_char_p, py_object)
tp_vectorcall = (py_object, py_object, py_object, c_ssize_t, py_object)
visitproc = (c_ssize_t, py_object, c_void_p)
tp_traverse_type = (c_ssize_t, py_object, *visitproc, c_void_p)
tp_new_type = (py_object, PyTypeObject, py_object, py_object)
sq_contains_type = (c_ssize_t, py_object, py_object)
nb_mul_type = (py_object, py_object, c_ssize_t)
bf_getbuffer_type = (c_int, py_object, c_void_p, c_int)
bf_releasebuffer_type = (c_void_p, py_object, c_void_p)

# Common function ctypes
c_int_ternary = CFUNCTYPE(*int_ternary)
c_unary = CFUNCTYPE(*unary)
c_binary = CFUNCTYPE(*binary)
c_ternary = CFUNCTYPE(*ternary)
c_ssize_unary = CFUNCTYPE(*ssize_unary)
c_index_f = CFUNCTYPE(*index_f)
c_iassign_f = CFUNCTYPE(*iassign_f)
c_init_f = CFUNCTYPE(*init_f)

# Additional ctypes for type object structure
c_destructor_type = CFUNCTYPE(*destructor_type)
c_tp_richcompare_type = CFUNCTYPE(*tp_richcompare_type)
c_ssize_ternary = CFUNCTYPE(*ssize_ternary)
c_tp_getattr_type = CFUNCTYPE(*tp_getattr_type)
c_tp_setattr_type = CFUNCTYPE(*tp_setattr_type)
c_tp_vectorcall = CFUNCTYPE(*tp_vectorcall)
c_visitproc = CFUNCTYPE(*visitproc)
c_tp_traverse_type = CFUNCTYPE(*tp_traverse_type)
c_tp_new_type = CFUNCTYPE(*tp_new_type)
c_sq_contains_type = CFUNCTYPE(*sq_contains_type)
c_nb_mul_type = CFUNCTYPE(*nb_mul_type)
c_bf_getbuffer_type = CFUNCTYPE(*bf_getbuffer_type)
c_bf_releasebuffer_type = CFUNCTYPE(*bf_releasebuffer_type)


class PyNumberMethods(Structure):
    _fields_ = [
        ('nb_add', c_binary),
        ('nb_subtract', c_binary),
        ('nb_multiply', c_binary),
        ('nb_remainder', c_binary),
        ('nb_divmod', c_binary),
        ('nb_power', c_ternary),
        ('nb_negative', c_unary),
        ('nb_positive', c_unary),
        ('nb_absolute', c_unary),
        ('nb_bool', c_ssize_unary),
        ('nb_invert', c_unary),
        ('nb_lshift', c_binary),
        ('nb_rshift', c_binary),
        ('nb_and', c_binary),
        ('nb_xor', c_binary),
        ('nb_or', c_binary),
        ('nb_int', c_unary),
        ('nb_reserved', c_void_p),
        ('nb_float', c_unary),
        ('nb_inplace_add', c_binary),
        ('nb_inplace_subtract', c_binary),
        ('nb_inplace_multiply', c_binary),
        ('nb_inplace_remainder', c_binary),
        ('nb_inplace_power', c_ternary),
        ('nb_inplace_lshift', c_binary),
        ('nb_inplace_rshift', c_binary),
        ('nb_inplace_and', c_binary),
        ('nb_inplace_xor', c_binary),
        ('nb_inplace_or', c_binary),
        ('nb_floor_divide', c_binary),
        ('nb_true_divide', c_binary),
        ('nb_inplace_floor_divide', c_binary),
        ('nb_inplace_true_divide', c_binary),
        ('nb_index', c_unary),
    ]


class PySequenceMethods(Structure):
    _fields_ = [
        ('sq_length', c_ssize_unary),
        ('sq_concat', c_binary),
        ('sq_repeat', c_index_f),
        ('sq_item', c_index_f),
        ('sq_slice', c_void_p),
        ('sq_ass_item', c_iassign_f),
        ('sq_ass_slice', c_void_p),
        ('sq_contains', c_sq_contains_type),
        ('sq_inplace_concat', c_binary),
        ('sq_inplace_repeat', c_index_f),
    ]


class PyMappingMethods(Structure):
    _fields_ = [
        ('mp_length', c_ssize_unary),
        ('mp_subscript', c_binary),
        ('mp_ass_subscript', c_int_ternary),
    ]


class PyAsyncMethods(Structure):
    _fields_ = [
        ('am_await', c_unary),
        ('am_aiter', c_unary),
        ('am_anext', c_unary),
        (
            'am_send',
            c_binary,
        ),
    ]


class PyBufferProcs(Structure):
    _fields_ = [
        ('bf_getbuffer', c_bf_getbuffer_type),
        ('bf_releasebuffer', c_bf_releasebuffer_type),
    ]


py_type_object_structs = {
    'tp_as_async': PyAsyncMethods,
    'tp_as_number': PyNumberMethods,
    'tp_as_sequence': PySequenceMethods,
    'tp_as_mapping': PyMappingMethods,
    'tp_as_buffer': PyBufferProcs,
}

METHOD_MAPPING: dict[str, tuple[str, Optional[str], tuple[type, ...]]] = {
    '__repr__': ('tp_repr', None, unary),
    '__call__': ('tp_call', None, unary),
    '__str__': ('tp_str', None, unary),
    '__getattribute__': ('tp_getattro', None, binary),
    '__setattr__': (
        'tp_setattro',
        None,
        ssize_ternary,
    ),
    '__init__': (
        'tp_init',
        None,
        ssize_ternary,
    ),
    '__new__': (
        'tp_new',
        None,
        tp_new_type,
    ),
    '__iter__': ('tp_iter', None, unary),
    '__next__': ('tp_iternext', None, unary),
    'comparison': (
        'tp_richcompare',
        None,
        tp_richcompare_type,
    ),
    '__hash__': ('tp_hash', None, ssize_unary),
    '__del__': ('tp_finalize', None, destructor_type),
    # Asynchronous execution methods mappings
    '__await__': ('tp_as_async', 'am_await', unary),
    '__aiter__': ('tp_as_async', 'am_aiter', unary),
    '__anext__': ('tp_as_async', 'am_anext', unary),
    # Numeric operations mappings
    '__sub__': ('tp_as_number', 'nb_subtract', binary),
    '__mod__': ('tp_as_number', 'nb_remainder', binary),
    '__divmod__': ('tp_as_number', 'nb_divmod', binary),
    '__pow__': ('tp_as_number', 'nb_power', ternary),
    '__neg__': ('tp_as_number', 'nb_negative', unary),
    '__pos__': ('tp_as_number', 'nb_positive', unary),
    '__abs__': ('tp_as_number', 'nb_absolute', unary),
    '__bool__': ('tp_as_number', 'nb_bool', ssize_unary),
    '__invert__': ('tp_as_number', 'nb_invert', unary),
    '__lshift__': ('tp_as_number', 'nb_lshift', binary),
    '__rshift__': ('tp_as_number', 'nb_rshift', binary),
    '__and__': ('tp_as_number', 'nb_and', binary),
    '__xor__': ('tp_as_number', 'nb_xor', binary),
    '__or__': ('tp_as_number', 'nb_or', binary),
    '__int__': ('tp_as_number', 'nb_int', unary),
    # nb_reserved
    '__float__': ('tp_as_number', 'nb_float', unary),
    '__iadd__': ('tp_as_number', 'nb_inplace_add', binary),
    '__isub__': ('tp_as_number', 'nb_inplace_subtract', binary),
    '__imod__': ('tp_as_number', 'nb_inplace_remainder', binary),
    '__ipow__': ('tp_as_number', 'nb_inplace_power', ternary),
    '__ilshift__': ('tp_as_number', 'nb_inplace_lshift', binary),
    '__irshift__': ('tp_as_number', 'nb_inplace_rshift', binary),
    '__iand__': ('tp_as_number', 'nb_inplace_and', binary),
    '__ixor__': ('tp_as_number', 'nb_inplace_xor', binary),
    '__ior__': ('tp_as_number', 'nb_inplace_or', binary),
    '__truediv__': ('tp_as_number', 'nb_true_divide', binary),
    '__floordiv__': ('tp_as_number', 'nb_floor_divide', binary),
    '__itruediv__': ('tp_as_number', 'nb_inplace_true_divide', binary),
    '__ifloordiv__': ('tp_as_number', 'nb_inplace_floor_divide', binary),
    '__index__': ('tp_as_number', 'nb_index', unary),
    # Sequence operations mappings
    '__contains__': (
        'tp_as_sequence',
        'sq_contains',
        sq_contains_type,
    ),
    '__rmul__': (
        'tp_as_sequence',
        'sq_repeat',
        index_f,
    ),
    '__iadd__': ('tp_as_sequence', 'sq_inplace_concat', binary),
    '__imul__': (
        'tp_as_sequence',
        'sq_inplace_repeat',
        index_f,
    ),
}

numeric_classes = {bool, int, float, complex}
sequence_classes = {
    str,
    list,
    tuple,
    range,
    memoryview,
    set,
    frozenset,
    dict_items_type,
    dict_keys_type,
    dict_values_type,
    deque,
}


def get_function_mapping(
    class_: type, method_name: str
) -> Optional[tuple[str, Optional[str], tuple[type, ...]]]:
    """
    Return information about method which represents given method
    internally.

    Parameters
    ----------
    class_ (Optional[type]): class if the method belongs to a class,
    None otherwise
    method_name (str): name of the method

    Returns
    -------
    Optional:
        str: name of the method or structure
        Optinal[str]: name of method if its part of a structure,
        None otherwise
        Any: method type
    """
    match method_name:
        case '__add__':
            if class_ in numeric_classes:
                return ('tp_as_number', 'nb_add', binary)
            return ('tp_as_sequence', 'sq_concat', binary)

        case '__mul__':
            if class_ in numeric_classes:
                return ('tp_as_number', 'nb_multiply', binary)
            return (
                'tp_as_sequence',
                'sq_repeat',
                index_f,
            )

        case '__len__':
            if class_ in sequence_classes:
                return ('tp_as_sequence', 'sq_length', ssize_unary)
            return ('tp_as_mapping', 'mp_length', ssize_unary)

        case '__getitem__':
            if class_ in [deque]:
                return (
                    'tp_as_sequence',
                    'sq_item',
                    index_f,
                )
            return ('tp_as_mapping', 'mp_subscript', binary)

        case '__setitem__':
            if class_ in [deque]:
                return (
                    'tp_as_sequence',
                    'sq_ass_item',
                    iassign_f,
                )
            return (
                'tp_as_mapping',
                'mp_ass_subscript',
                int_ternary,
            )

        case _:
            return METHOD_MAPPING.get(method_name, None)


PyObject._fields_ = [
    ('ob_refcnt', c_ssize_t),
    ('ob_type', POINTER(PyTypeObject)),
]

PyTypeObject._fields_ = [
    # varhead
    ('ob_base', PyObject),
    ('ob_size', c_ssize_t),
    # declaration
    ('tp_name', c_char_p),
    ('tp_basicsize', c_ssize_t),
    ('tp_itemsize', c_ssize_t),
    ('tp_dealloc', c_destructor_type),
    ('tp_vectorcall_offset', c_ssize_t),
    ('tp_getattr', c_tp_getattr_type),
    ('tp_setattr', c_tp_setattr_type),
    ('tp_as_async', POINTER(PyAsyncMethods)),
    ('tp_repr', c_unary),
    ('tp_as_number', POINTER(PyNumberMethods)),
    ('tp_as_sequence', POINTER(PySequenceMethods)),
    ('tp_as_mapping', POINTER(PyMappingMethods)),
    ('tp_hash', c_ssize_unary),
    ('tp_call', c_ternary),
    ('tp_str', c_unary),
    ('tp_getattro', c_binary),
    ('tp_setattro', c_ssize_ternary),
    ('tp_as_buffer', POINTER(PyBufferProcs)),
    ('tp_flags', c_ulong),
    ('tp_doc', c_char_p),
    ('tp_traverse', c_tp_traverse_type),
    ('tp_clear', c_ssize_unary),
    ('tp_richcompare', c_tp_richcompare_type),
    ('tp_weaklistoffset', c_ssize_t),
    ('tp_iter', c_unary),
    ('tp_iternext', c_unary),
    ('tp_methods', c_void_p),
    ('tp_members', c_void_p),
    ('tp_getset', c_void_p),
    ('tp_base', c_void_p),
    ('tp_dict', py_object),
    ('tp_descr_get', c_ternary),
    ('tp_descr_set', c_ssize_ternary),
    ('tp_dictoffset', c_ssize_t),
    ('tp_init', c_ssize_ternary),
    ('tp_alloc', c_index_f),
    ('tp_new', c_tp_new_type),
    ('tp_free', c_destructor_type),
    ('tp_is_gc', c_destructor_type),
    ('tp_bases', py_object),
    ('tp_mro', py_object),
    ('tp_cache', py_object),
    ('tp_subclasses', py_object),
    ('tp_weaklist', py_object),
    ('tp_del', c_destructor_type),
    ('tp_version_tag', c_uint),
    ('tp_finalize', c_destructor_type),
    ('tp_vectorcall', c_tp_vectorcall),
    ('tp_watched', c_ubyte),
]
