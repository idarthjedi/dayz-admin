from abc import ABC, abstractmethod


class FileManager(ABC):

    @abstractmethod
    def __init__(self, pathname: str):
        self._pathname = pathname
        pass

    @abstractmethod
    def validate(self):
        pass
