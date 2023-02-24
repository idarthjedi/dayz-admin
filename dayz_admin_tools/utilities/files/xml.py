import xml.sax

from dayz_admin_tools.utilities.files.fManager import FileManager
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
"""XML File Manager

Creates an Instance of a XML File for various Management functions
"""


class XMLManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        """

        :param filepath: location of the directories & subdirectories to search for JSON files
        :return: Tuple (SUCCESS_STATUS, FAILED_FILES)
        """

        validated = True
        output = []
        file_count = 0

        files = super(XMLManager, XMLManager).find_files(filepath, ".xml")

        for file in files:
            # with open(file) as validate_file:
            try:

                parser = make_parser()
                parser.setContentHandler(ContentHandler())
                parser.parse(file)

                file_count += 1
            except xml.sax.SAXParseException as error:
                output.append(file)
                validated = False

        return validated, file_count, output

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    pass
