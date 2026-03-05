import json

from dayz_admin_tools.utilities.files.fManager import FileManager


class JSONManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        validated = True
        output = []
        file_count = 0

        files = FileManager.find_files(filepath, ".json")
        for file in files:
            with open(file) as validate_file:
                try:
                    json.load(validate_file)
                    file_count += 1
                except json.JSONDecodeError:
                    output.append(file)
                    validated = False

        return validated, file_count, output
