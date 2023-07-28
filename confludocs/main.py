from __future__ import annotations

import sys
import inspect
import pathlib
import importlib


def detect_lib_in_dir(path):
    """Get Path of folder containing library within directory.

    The function looks for a directory directly under this one which contains
    some file named "__init__.py".

    Args:
        path (str): String containing directory path
    """
    top_level = False
    if isinstance(path, str):
        top_level = True
        path = pathlib.Path(path)

    for item in path.iterdir():
        if item.name == "__init__.py":
            if top_level:
                return item
            else:
                return True
        elif item.is_dir():
            if detect_lib_in_dir(item):
                return item
    return False


dir_path_str = "/Users/endrebjorgo/Documents/Utvikling/Prosjekter/dummylib/"
dir_path = pathlib.Path(dir_path_str)

lib_path = detect_lib_in_dir(dir_path_str)
lib_name = lib_path.name

sys.path.append(dir_path_str)
# lib = importlib.import_module(lib_name)  lib.pkg.mod...


def import_submodules(lib_path, curr_path=[lib_path.stem]):
    for item in lib_path.iterdir():
        if item.name in ["__pycache__", "__init__.py"]:
            continue

        this_path = curr_path + [item.stem]

        import_str = ".".join(this_path)
        importlib.import_module(import_str)

        if item.is_dir():
            import_submodules(item, this_path)


import_submodules(lib_path)

for mod in sys.modules.copy():
    print(mod)

clsmembers = inspect.getmembers(sys.modules["dummylib"], inspect.isclass)
print(clsmembers)

"""
To do time:
- Get a list of all import strings (lib.pkg.mod...) so that they can be
  analyzed with getmembers.
- Generate markdown from the module
- Analyzing functions:
 - name = func.__name__
 - variables = func.__code__.co_varnames
 - docstring = func.__doc__
"""
