class BaseProvider(object):

    @classmethod
    def providersFor(cls):
        return cls.provides_for

    @classmethod
    def getProviders(cls):
        _providers = {}
        for _provider in cls.__subclasses__():
            _provides_for = _provider.provides_for
            _providers[_provides_for] = _provider
        return _providers

    @classmethod
    def getProvider(cls, hostname):
        _providers = cls.getProviders()
        if hostname in _providers.keys():
            return _providers.get(hostname)
        else:
            raise Exception("No provider for {0}".format(hostname))
