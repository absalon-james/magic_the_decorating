import sys

from config import load as load_config
from loaders import CallableLoader, ModuleLoader


class Finder(object):
    """
    Custom importer that should follow 302.

    """
    def __init__(self, config_filename):
        """
        Inits the finder. Accepts a file name containing yaml dictionary
        describing how to decorate imports.

        """
        self.config_filename = config_filename
        self.config = load_config(self.config_filename)

        callable_loader = CallableLoader()
        self.callables = {}
        for module_name, module_config in self.config.items():
            self.callables[module_name] = \
                callable_loader.load(module_config['callable'])

    def find_module(self, fullname, path=None):
        """
        Method to find a module. Check if module is one we are intrested in.
        Return None if not interested. A finder if interested

        """
        if fullname in self.config:
            return Loader(path,
                          self.callables[fullname],
                          self.config[fullname].get('config'))
        return None


class Loader(object):
    """
    Custom loader that should follow 302.

    """
    decorated_key = '__magic_the_decorated__'

    def __init__(self, path, callable_, callable_config):
        """
        @param path - Path passed to find module
        @param callable_ - Callable to apply to module
        @param callable_config - Dictionary to configure callable

        """
        self._path = path
        self._callable = callable_
        self._callable_config = callable_config

    def is_decorated(self, module):
        """
        Return whether or not the object had an attribute set indicating
        that it has already been decorated.

        @param module - Module to check
        @return Boolean

        """
        return hasattr(module, self.decorated_key)

    def set_decorated(self, module):
        """
        Sets the decorated attribute.

        @param module - Module to flag as decorated

        """
        setattr(module, self.decorated_key, True)

    def load_module(self, fullname):
        """
        If an existing object named fullname is in sys.modules,
        the loader must use that module before running code.

        If sys.modules does not contain fullname, then a new module
        object must be added to sys.modules before running any code.

        If the load fails, the loader needs to remove any module that may
        have been inserted into sys.modules. If the module was already
        in sys.modules, the loader needs to leave it alone.

        A loaded module must have the __file__ attribute set
        A loaded module must have the __name__ attribute set
        A loaded module must have the __loader__ attribute set
            - should be this module

        The package attribute should be set
        """
        if fullname in sys.modules:
            module = sys.modules[fullname]
            existing = True
        else:
            module = ModuleLoader().load(fullname, self._path)
            existing = False

        if not self.is_decorated(module):
            try:
                module = self._callable(module, self._callable_config)
                self.set_decorated(module)
            except Exception:
                if fullname in sys.modules and not existing:
                    del sys.modules[fullname]
        return module
