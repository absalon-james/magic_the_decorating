# Use imp for module loading.
import imp

# Use importlib for callable loading.
import importlib


class ModuleLoader(object):
    """
    Loads a module by name.

    """
    def load(self, name, path):
        """
        Load module.

        @param name - String name of module
        @param path - List of string paths
        @return Module
        @raises ImportError

        """
        module_name = name
        if path is not None:
            package_name, module_name = module_name.rsplit('.', 1)
        module_info = imp.find_module(module_name, path)
        return imp.load_module(name, *module_info)


class CallableException(Exception):
    pass


class CallableLoader(object):
    """
    Loades a modules and returns a callable from the module.

    """
    def load(self, callable_name):
        """
        Load callable

        @param callable_name - String full python path to callable
            callable should be a root level attribute to a module.
            example: somepackage.somemodule.some_func

        @returns - Callable

        """
        try:
            original_name = callable_name
            module_name, callable_name = callable_name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            _callable = getattr(module, callable_name)
            if hasattr(_callable, '__call__'):
                return _callable
            else:
                raise CallableException("%s is not callable." % original_name)
        except ValueError:
            raise CallableException(
                "Missing module in callable decoration: %s" % original_name
            )
