import sys
import inspect
import pathlib
import importlib


class DistributionPackage:
    """An implementation of a distribution package.
    
    Refers to a directory containing source code and related files which is downloaded by the user.
    """

class ImportPackage:
    """An implementation of an import package.
    
    Refers to a directory containing python modules and/or other import packages.
    """

class Module:
    """An implementation of a module.
    
    Refers to a python module which takes the form of a single python file.
    """