import os
import shutil
from datetime import datetime


class FileManager:
    """Base file manager with shared static utilities."""

    @staticmethod
    def backup(fullpath_filename: str) -> None:
        uniqueness_name = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        file_parts = os.path.splitext(fullpath_filename)
        new_filename = f"{file_parts[0]}-BACKUP.{uniqueness_name}.{file_parts[1]}"
        shutil.copy(fullpath_filename, new_filename)

    @staticmethod
    def return_filename(fullpath_filename: str, split_extension: bool = False) -> tuple:
        if not split_extension:
            return os.path.basename(fullpath_filename)
        else:
            return os.path.splitext(fullpath_filename)

    @staticmethod
    def return_dirname(fullpath_filename: str) -> str:
        return os.path.dirname(fullpath_filename)

    @staticmethod
    def find_files(filepath: str, extension: str) -> list:
        file_names = []
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(extension) and not file.startswith("."):
                    file_names.append(os.path.join(root, file))
        return file_names
