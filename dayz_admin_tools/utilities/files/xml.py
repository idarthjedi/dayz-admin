from . fManager import FileManager
"""XML File Manager

Creates an Instance of an XML File for various Management functions
"""


class XMLManager(FileManager):

    def __init__(self, pathname: str):
        super().__init__(pathname)
        pass

    def validate(self):
        print(f"Validating {self._pathname} XML file!")
        pass


if __name__ == "__main__":
    file1 = XMLManager("file.xml")