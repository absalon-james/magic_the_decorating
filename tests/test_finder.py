import mock
import unittest

from magic_the_decorating import importer

mock_callable_config = {
    'param1': 'value1',
    'param2': 'value2'
}

mock_config = {
    'fake_package.fake_module': {
        'callable': 'fake_package.fake_module.fake_callables.callable',
        'config': mock_callable_config
    }
}

mock_config_with_none = {
    'fake_package.fake_module': {
        'callable': 'fake_package.fake_module.fake_callables.callable'
    }
}


class TestFinder(unittest.TestCase):
    """
    Tests for importer module finder.

    """
    @mock.patch('magic_the_decorating.importer.load_config',
                return_value=mock_config)
    @mock.patch('magic_the_decorating.importer.CallableLoader.load',
                return_value='fake_callable')
    def test_config(self, mocked_callable_loader, mocked_load_config):
        """
        Tests that load config is called with the correct file name

        """
        config_filename = 'aconfigfile'
        finder = importer.Finder(config_filename)
        mocked_load_config.assert_called_once_with(config_filename)

        module_config = finder.config.get('fake_package.fake_module')
        self.assertTrue(module_config is not None)
        self.assertTrue('callable' in module_config)
        self.assertTrue('config' in module_config)

    @mock.patch('magic_the_decorating.importer.load_config',
                return_value=mock_config)
    @mock.patch('magic_the_decorating.importer.Loader')
    @mock.patch('magic_the_decorating.importer.CallableLoader.load',
                return_value='fake_callable')
    def test_module_in_config(self, mocked_callable_loader,
                              mocked_loader, mocked_config):
        """
        Tests the finder.find_module method for a module that is listed in the
        finder configuration.

        """
        config_filename = 'aconfigfile'
        finder = importer.Finder(config_filename)

        fullname = 'fake_package.fake_module'
        path = None
        finder.find_module(fullname, path)
        mocked_loader.assert_called_once_with(path, 'fake_callable',
                                              mock_callable_config)

    @mock.patch('magic_the_decorating.importer.load_config',
                return_value=mock_config_with_none)
    @mock.patch('magic_the_decorating.importer.CallableLoader.load',
                return_value='fake_callable')
    def test_none_in_config(self, mocked_callable_loader, mocked_load_config):
        """
        Tests loading config with a module callable that has no config.

        """
        config_filename = 'aconfigfile'
        importer.Finder(config_filename)
