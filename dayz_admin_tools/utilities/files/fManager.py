from abc import ABC, abstractmethod
from datetime import datetime

import os
import shutil


class FileManager(ABC):

    @abstractmethod
    def __init__(self):
        """
        Creates a copy of the File Manager
        """
        pass

    @staticmethod
    def backup(fullpath_filename: str) -> bool:
        uniqueness_name = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        file_parts = os.path.splitext(fullpath_filename)
        new_filename = f"{file_parts[0]}-BACKUP.{uniqueness_name}.{file_parts[1]}"

        shutil.copy(fullpath_filename, new_filename)


    @staticmethod
    @abstractmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        """

        :return: True if all files validated, otherwise false
        """
        pass

    @staticmethod
    def find_files(filepath: str, extension: str) -> list:
        """

        :param filepath:
        :param extension:
        :return:
        """
        file_names = []
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(extension) and not file.startswith("."):
                    file_names.append(os.path.join(root, file))

        return file_names

