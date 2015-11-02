import os
import sys
import unittest

from magic_the_decorating.loaders import ModuleLoader


class TestLoader(unittest.TestCase):
    """
    Tests for loading modules.

    """
    def test_bad_module(self):
        """
        Tests the loading of a module that would cause an import error.

        """
        with self.assertRaises(ImportError):
            ModuleLoader().load('mumbojumbo', None)

    def test_load_good_module(self):
        """
        Tests loading existing module.

        """
        test_module_path = os.path.join(os.path.dirname(__file__),
                                        'data',
                                        'packages')
        try:
            sys.path.append(test_module_path)
            fullname = 'fake_package.fake_module'
            path = [
                '/root/magic_the_decorating/tests/data/packages/fake_package'
            ]
            module = ModuleLoader().load(fullname, path)
            self.assertTrue(hasattr(module, 'fake_func'))
        finally:
            if test_module_path in sys.path:
                sys.path.remove(test_module_path)
