import xml.sax
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from dayz_admin_tools.utilities.files.fManager import FileManager


class XMLManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        validated = True
        output = []
        file_count = 0

        files = FileManager.find_files(filepath, ".xml")

        for file in files:
            try:
                parser = make_parser()
                parser.setContentHandler(ContentHandler())
                parser.parse(file)
                file_count += 1
            except xml.sax.SAXParseException:
                output.append(file)
                validated = False

        return validated, file_count, output
