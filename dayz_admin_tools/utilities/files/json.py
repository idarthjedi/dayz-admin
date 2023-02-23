from dayz_admin_tools.utilities.files.fManager import FileManager
import json
import os
"""JSON File Manager

File Manager for JSON objects 
"""


class JSONManager(FileManager):
    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, list]:
        """

        :param filepath: location of the directories & subdirectories to search for JSON files
        :return: Tuple (SUCCESS_STATUS, FAILED_FILES)
        """

        validated = True
        output = []

        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(".json") and not file.startswith("."):
                    filename = os.path.join(root, file)
                    with open(filename) as validate_file:
                        try:
                            json.load(validate_file)
                        except json.JSONDecodeError as error:
                            output.append(filename)
                            validated = False

        return validated, output

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass
