import yaml


def load(filename):
    """
    Expects the file at filename to be a yaml file. Returns the parsed
    configuration.

    """
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config
