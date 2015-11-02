import os
import sys
import unittest

from magic_the_decorating.loaders import CallableLoader, CallableException


class TestLoader(unittest.TestCase):
    """
    Tests for loading modules.

    """
    def test_incomplete_callable_name(self):
        """
        Tests loading of callable where module is unspecified.
        Should raise a callable exception.

        """
        callable_name = 'thefunc'
        with self.assertRaises(CallableException):
            CallableLoader().load(callable_name)

    def test_bad_module(self):
        """
        Tests the loading of a callable that should raise an import error

        """
        callable_name = 'mumbojumbo.thefunc'
        with self.assertRaises(ImportError):
            CallableLoader().load(callable_name)

    def test_bad_attribute(self):
        """
        Tests the loading of callable whose module exists but the callable
        does not.

        """
        callable_name = 'fake_package.fake_module.func_that_does_not_exist'
        test_module_path = os.path.join(os.path.dirname(__file__),
                                        'data',
                                        'packages')
        try:
            sys.path.append(test_module_path)
            with self.assertRaises(AttributeError):
                CallableLoader().load(callable_name)()
        finally:
            if test_module_path in sys.path:
                sys.path.remove(test_module_path)

    def test_load_good_module(self):
        """
        Tests loading existing callable.

        """
        callable_name = 'fake_package.fake_module.fake_func'
        test_module_path = os.path.join(os.path.dirname(__file__),
                                        'data',
                                        'packages')
        try:
            sys.path.append(test_module_path)
            CallableLoader().load(callable_name)()
        finally:
            if test_module_path in sys.path:
                sys.path.remove(test_module_path)
