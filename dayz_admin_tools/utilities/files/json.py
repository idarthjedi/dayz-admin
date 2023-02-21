from . fManager import FileManager
"""JSON File Manager

Creates an Instance of a JSON File for various Management functions
"""


class JSONManager(FileManager):

    def __init__(self, pathname: str):
        super().__init__(pathname)
        pass

    def validate(self):
        print(f"Validating {self._pathname} JSON file!")
        pass


if __name__ == "__main__":
    file1 = JSONManager("file.json")



