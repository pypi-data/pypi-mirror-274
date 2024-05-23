# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module used for lazy loading of submodules.

"""
import importlib
import os
import sys
import types


class LazyLoader(types.ModuleType):
    """Lazily import a module, mainly to avoid pulling in large dependencies.

    This class acts as a proxy for a module, loading it only when an attribute
    of the module is accessed for the first time.

    Args:
        local_name: The local name that the module will be refered to as.
        parent_module_globals: The globals of the module where this should be imported.
            Typically this will be globals().
        name: The full qualified name of the module.
    """

    def __init__(self, local_name, parent_module_globals, name):
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals
        self._module = None
        self._docs_build = self._is_sphinx_build()
        super().__init__(name)

    def _is_sphinx_build(self):
        """Check if the current environment is a Sphinx build."""
        return os.environ.get("SPHINX_BUILD") == "1" or "sphinx" in sys.modules

    def _load(self):
        """Load the module and insert it into the parent's globals."""
        if self._module is None:
            self._module = importlib.import_module(self.__name__)
            self._parent_module_globals[self._local_name] = self._module
            self.__dict__.update(self._module.__dict__)
        return self._module

    def __getattr__(self, item):
        if self._docs_build:
            self._load()  # Ensure module is loaded when Sphinx is running
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        if self._docs_build:
            self._load()  # Ensure module is loaded when Sphinx is running
        module = self._load()
        return dir(module)
