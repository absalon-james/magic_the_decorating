import os
import sys
import unittest

from magic_the_decorating import importer


def fake_callable(module, config):
    """
    Sample fake callable. Simply adds an attribute we can test for

    @param module - Module to augment
    @param config - Unused by this callable

    """
    setattr(module, '__fake_callable__', True)
    return module


class FakeModule():
    """Fake module object"""
    pass


class TestImport(unittest.TestCase):
    """
    Tests an actual import using the import.Finder and import.Loader classes

    """
    test_module_path = os.path.join(os.path.dirname(__file__),
                                    'data',
                                    'packages')

    def setUp(self):
        """
        Adds fake packages to python class

        """
        sys.path.append(self.test_module_path)

    def tearDown(self):
        """
        Removes fake packages from python path
        Removes any modules that may have been inserted into sys.modules

        """
        sys.meta_path = []
        if self.test_module_path in sys.path:
            sys.path.remove(self.test_module_path)
        module_names = [
            'fake_package',
            'fake_package.fake_module'
        ]
        for name in module_names:
            if name in sys.modules:
                del sys.modules[name]

    def test_import(self):
        """
        Tests full import process

        """
        config_file = os.path.join(os.path.dirname(__file__),
                                   'data',
                                   'test_config.yaml')
        finder = importer.Finder(config_file)
        sys.meta_path.append(finder)

        import fake_package.fake_module
        self.assertTrue(hasattr(fake_package.fake_module, '__fake_callable__'))

        import fake_package
        self.assertTrue(hasattr(fake_package, '__fake_callable__'))
