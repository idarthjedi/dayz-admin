from dayz_admin_tools.utilities.files.fManager import FileManager

"""XML File Manager

Creates an Instance of a XML File for various Management functions
"""


class XMLManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, list]:
        pass

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass
