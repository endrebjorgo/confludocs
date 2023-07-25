from __future__ import annotations

import sys
import inspect
import pathlib
from pathlib import Path
import importlib


class DistributionPackage:
    """An implementation of a distribution package.
    
    Refers to a directory containing source code and related files which is downloaded by the user.
    """
    def __init__(self, dist_path: str | Path) -> None:
        self.path_obj: Path = Path(dist_path)
        self.name: str = self.path_obj.name
        self.contents: list = self._init_contents()
        self.src_pack: ImportPackage = self._detect_src() 

    def _init_contents(self):
        contents = list()
        for item in self.path_obj.iterdir():
            if item.is_dir():
                contents.append(ImportPackage(item, self))
            elif item.suffix == ".py":
                contents.append(Module(item, self))
            else:
                contents.append(Other(item, self))
        return contents

    def _detect_src(self) -> ImportPackage:
        for item1 in self.contents:
            if not isinstance(item1, ImportPackage):
                continue

            if item1._contains_init():
                return item1
            else:
                for item2 in item1.contents:
                    if isinstance(item2, ImportPackage) and item2._contains_init():
                        return item1
        else:
            print("ERROR: Could not detect any source code in the package.")
            exit(1)

class ImportPackage:
    """An implementation of an import package.
    
    Refers to a directory containing python modules and/or other import packages.
    """
    def __init__(self, import_path: str | Path, parent: ImportPackage | DistributionPackage) -> None:
        self.parent: ImportPackage | None = parent
        self.path_obj: Path = Path(import_path)
        self.name = self.path_obj.name
        self.import_string: str = self.path_obj.stem
        if isinstance(self.parent, ImportPackage):
            self.import_string: str = self.parent.import_string + '.' + self.import_string
        self.contents: list[Path] = self._init_contents()

    def _init_contents(self):
        contents = list()
        for item in self.path_obj.iterdir():
            if item.is_dir():
                contents.append(ImportPackage(item, self))
            elif item.suffix == ".py":
                contents.append(Module(item, self))
            else:
                contents.append(Other(item, self))
        return contents
    
    def _contains_init(self):
        for item in self.contents:
            if item.name == "__init__.py":
               return True
        return False 

class Module:
    """An implementation of a module.
    
    Refers to a python module which takes the form of a single python file.
    """
    
    def __init__(self, module_path: str | Path, parent: ImportPackage | DistributionPackage) -> None:
        self.parent: ImportPackage | DistributionPackage = parent
        self.path_obj: Path = Path(module_path)
        self.name: str = self.path_obj.name
        self.import_string = None
        if isinstance(self.parent, ImportPackage):
            self.import_string: str = self.parent.import_string + '.' + self.path_obj.stem


class Other:
    def __init__(self, other_path: str | Path, parent: ImportPackage | DistributionPackage) -> None:
        self.path_obj: Path = Path(other_path)
        self.name: str = self.path_obj.name


d = DistributionPackage("/Users/endrebjorgo/Documents/Utvikling/Prosjekter/dummylib/")

print(d.src_pack.name)

for e in d.contents:
    print(e.path_obj)

