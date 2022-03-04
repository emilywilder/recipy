from .base import BaseProvider
from .exceptions import NoProviderException


def get_providers() -> dict:
    """return a dictionary of providers in the format:

    { provides_for: <class Provider> }

    where each key is a hostname and the value is the
    provider class for that hostname
    """
    return dict([
        (x.provides_for, x) for x in BaseProvider.__subclasses__()
    ])


def get_provider(hostname: str) -> BaseProvider:
    """return the appropriate provider class by hostname"""
    _providers = get_providers()
    if hostname in _providers.keys():
        return _providers.get(hostname)
    else:
        raise NoProviderException(hostname)
