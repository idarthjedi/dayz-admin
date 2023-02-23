from abc import ABC, abstractmethod


class FileManager(ABC):

    @abstractmethod
    def __init__(self):
        """
        Creates a copy of the File Manager
        """
        pass

    @staticmethod
    @abstractmethod
    def validate_files(filepath: str) -> tuple[bool, list]:
        """

        :return: True if all files validated, otherwise false
        """
        pass
