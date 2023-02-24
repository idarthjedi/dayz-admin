from dayz_admin_tools.utilities.files.fManager import FileManager
import json
import os
"""JSON File Manager

File Manager for JSON objects 
"""


class JSONManager(FileManager):
    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        """

        :param filepath: location of the directories & subdirectories to search for JSON files
        :return: Tuple (SUCCESS_STATUS, FAILED_FILES)
        """

        validated = True
        output = []
        file_count = 0

        files = super(JSONManager, JSONManager).find_files(filepath, ".json")
        for file in files:
            with open(file) as validate_file:
                try:
                    json.load(validate_file)
                    file_count += 1
                except json.JSONDecodeError as error:
                    output.append(file)
                    validated = False

        return validated, file_count, output

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass
