import mock
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


class TestLoader(unittest.TestCase):
    """
    Tests for importer module loader

    """
    test_module_path = os.path.join(os.path.dirname(__file__),
                                    'data',
                                    'packages')

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
    """

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
        if self.test_module_path in sys.path:
            sys.path.remove(self.test_module_path)
        module_names = [
            'fake_package',
            'fake_package.fake_module'
        ]
        for name in module_names:
            if name in sys.modules:
                del sys.modules[name]

    def test_init(self):
        """
        Tests the init method

        """
        path = None
        _callable = 'fake_callable'
        config = 'fake_callable_config'
        loader = importer.Loader(path, _callable, 'fake_callable_config')
        self.assertTrue(loader._path is None)
        self.assertEquals(loader._callable, _callable)
        self.assertEquals(loader._callable_config, config)

    def test_is_decorated(self):
        """
        Tests the is_decorated method of the loader.

        """
        loader = importer.Loader(None, None, None)
        module = FakeModule()
        self.assertFalse(loader.is_decorated(module))

        setattr(module, '__magic_the_decorated__', True)
        self.assertTrue(loader.is_decorated(module))

    def test_set_decorated(self):
        """
        Tests the set_decorated method of the loader

        """
        module = FakeModule()
        loader = importer.Loader(None, None, None)
        loader.set_decorated(module)
        self.assertTrue(hasattr(module, '__magic_the_decorated__'))

    def test_new_module(self):
        """
        Tests a module that has not been imported yet

        """
        fullname = 'fake_package.fake_module'
        path = ['/root/magic_the_decorating/tests/data/packages/fake_package']
        mock_callable = mock.Mock(side_effect=fake_callable)
        self.assertFalse(fullname in sys.modules)
        loader = importer.Loader(path, mock_callable, None)
        result = loader.load_module(fullname)
        self.assertTrue(hasattr(result, 'fake_func'))
        self.assertTrue(hasattr(result, '__magic_the_decorated__'))
        self.assertTrue(result is sys.modules[fullname])

    def test_existing_undecorated(self):
        """
        Tests a module already in sys.modules that is not decorated.

        """
        mock_callable = mock.Mock(side_effect=fake_callable)
        config = {}
        fullname = 'fake_package.fake_module'
        path = '/root/magic_the_decorating/tests/data/packages/fake_package'
        sys.modules[fullname] = FakeModule()
        loader = importer.Loader(path, mock_callable, config)
        result = loader.load_module(fullname)
        self.assertTrue(isinstance(result, FakeModule))
        self.assertTrue(mock_callable.called)
        self.assertTrue(hasattr(result, '__magic_the_decorated__'))
        self.assertTrue(hasattr(result, '__fake_callable__'))

    def test_existing_decorated(self):
        """
        Tests a module already in sys.modules that is already decorated

        """
        mock_callable = mock.Mock(side_effect=fake_callable)
        config = {}
        fullname = 'fake_package.fake_module'
        path = '/root/magic_the_decorating/tests/data/packages/fake_package'
        fake_module = FakeModule()
        setattr(fake_module, '__magic_the_decorated__', True)
        sys.modules[fullname] = fake_module
        loader = importer.Loader(path, mock_callable, config)
        result = loader.load_module(fullname)
        self.assertTrue(isinstance(result, FakeModule))
        self.assertFalse(hasattr(result, '__fake_callable__'))
        mock_callable.assert_not_called()

    def test_reload(self):
        """
        Tests a module already in sys.modules that is reloaded

        """
        pass
