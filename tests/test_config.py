import unittest

from os import path
from yaml import YAMLError

from magic_the_decorating import config


class TestConfig(unittest.TestCase):
    """
    Tests the loading of configuration for magic_the_decorating.

    """
    def test_valid_config(self):
        """
        Load a sample config from the data directory.

        """
        config_file = path.join(path.dirname(__file__),
                                'data',
                                'valid_config.yaml')
        conf = config.load(config_file)
        for module_key, module_value in conf.iteritems():
            self.assertEquals(module_key, 'module_key')
            self.assertEquals(module_value['callable'], 'callable_value')
            self.assertEquals(module_value['config'], 'config_value')

    def test_invalid_config(self):
        """
        Tests that a yaml error is raised with improper yaml

        """
        config_file = path.join(path.dirname(__file__),
                                'data',
                                'invalid_config.yaml')
        with self.assertRaises(YAMLError):
            config.load(config_file)

    def test_invalid_file(self):
        """
        Tests that loading from an invalid file raises an exception.

        """
        config_file = 'mumbo_jumbo'
        with self.assertRaises(IOError):
            config.load(config_file)
