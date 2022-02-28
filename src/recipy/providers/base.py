from recipy.providers.exceptions import NoProviderException


class BaseProvider(object):

    @classmethod
    def providersFor(cls):
        return cls.provides_for

    @classmethod
    def getProviders(cls):
        '''return a dictionary of providers in the format:

        { provides_for: <class Provider> }

        where each key is a hostname and the value is the provider class for that hostname
        '''
        return dict([(x.provides_for, x) for x in cls.__subclasses__()])

    @classmethod
    def getProvider(cls, hostname):
        _providers = cls.getProviders()
        if hostname in _providers.keys():
            return _providers.get(hostname)
        else:
            raise NoProviderException(hostname)
