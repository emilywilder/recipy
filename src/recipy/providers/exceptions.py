class ProviderException(Exception):
    pass


class NoProviderException(ProviderException):
    def __init__(self, hostname) -> None:
        self.message = "No provider for {0}".format(hostname)
