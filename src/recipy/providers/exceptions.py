class ProviderException(Exception):
    pass


class NoProviderException(ProviderException):
    def __init__(self, hostname) -> None:
        self.hostname = hostname

    def __str__(self) -> str:
        return "No provider for {0}".format(self.hostname)
