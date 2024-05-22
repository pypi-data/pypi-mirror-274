from types import ModuleType
import inspect
import os
import sys
from typing import Any, Callable
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec


def get_module_by_name(module_name: str) -> ModuleType:
    """
    Returns a module with given name.

    Parameters
    ----------
    module_name (str): name of a module

    Returns
    -------
    ModuleType: module with given name

    Exception
    -------
    Raises exception if the module does not exist.
    """
    try:
        return sys.modules[module_name]
    except KeyError:
        raise ImportError(f'Unkown module: {module_name}')


def is_std_module(module: ModuleType) -> bool:
    """
    Determines if module is standard module.

    Parameters
    ----------
    module (ModuleType): module

    Returns
    -------
    bool: information if the module is a standard module
    """
    parent_module = module.__name__.split('.')[0]

    return parent_module in sys.stdlib_module_names


def is_user_defined_module(module: ModuleType) -> bool:
    """
    Determines if module was defined by user.

    Parameters
    ----------
    module (ModuleType): module

    Returns
    -------
    bool: information if module was defined by user
    """
    # To check if the module is defined by the user
    # try to get the module's file path
    # if the module is builtin, inspect.getfile will raise a TypeError
    try:
        module_file = inspect.getfile(module)
    except TypeError:
        return False

    std_lib_path = os.path.dirname(os.__file__)
    site_packages_paths = [
        site_package_path
        for site_package_path in sys.path
        if 'site-packages' in site_package_path
    ]

    if module_file.startswith(std_lib_path) or any(
        module_file.startswith(path) for path in site_packages_paths
    ):
        return False
    else:
        return True


def get_module_imports(
    module: ModuleType, ignored_modules: set[ModuleType]
) -> tuple[set[ModuleType], set[Callable[..., Any]]]:
    """
    Returns all modules and callables imported by module
    and of those modules recursively.

    Parameters
    ----------
    module (ModuleType): module
    ignored_modules (set): set of modules that are not to be included
    Returns
    -------
    set: all modules imported by given module
    set: all callables imported by given module
    """
    imported_modules = set()
    imported_functions = set()
    for _, obj in vars(module).items():
        if isinstance(obj, ModuleType):
            if obj not in ignored_modules:
                imported_modules.add(obj)
        elif (
            callable(obj)
            and hasattr(obj, '__module__')
            and obj.__module__ != module.__name__
        ):
            if get_module_by_name(obj.__module__) not in ignored_modules:
                imported_functions.add(obj)

    subimports = set()
    for module in imported_modules:
        if is_user_defined_module(module):
            imps, funcs = get_module_imports(module, ignored_modules)
            subimports.update(imps)
            imported_functions.update(funcs)

    imported_modules.update(subimports)

    return imported_modules, imported_functions


def import_from_path(file_path: str) -> ModuleType:
    """
    Imports a module from given path.

    Parameters
    ----------
    file_path (str): path to a file with module definition

    Returns
    -------
    ModuleType: module defined on given path
    """
    path = Path(file_path).resolve()
    module_name = path.stem

    spec = spec_from_file_location(module_name, str(path))
    if spec and spec.loader:
        module = module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    raise ImportError(f'Could not load module from path: {file_path}')


def insert_module_to_path(input_file: str) -> None:
    """
    Inserts module of the input file to path.

    Parameters
    ----------
    input_file (str): path to the input file

    Returns
    -------
    None
    """
    module_dir = os.path.dirname(input_file)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
