def test_callable(module, config):
    setattr(module, '__fake_callable__', True)
    return module
