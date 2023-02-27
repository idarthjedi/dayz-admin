import os

from lxml import etree
from dayz_admin_tools.config import ROOT_DIR
from jsonschema import validate as json_validate
from dayz_admin_tools.utilities.files.fManager import FileManager

from dayz_admin_tools.utilities.economy.Type import Type
from colorama import Fore, Back, Style


class Items(dict):
    # _types = {}

    def __init__(self):
        # load the XSD file
        with open(ROOT_DIR + "/dayz_admin_tools/utilities/traders/expansion/schemas/items.schema.json", "r") as schema_doc:
            self._jsonschema = schema_doc.read()
        super().__init__()

    @staticmethod
    def find_item_files(root_directory: str) -> tuple[bool, list]:
        """

        :param root_directory: Provide the root directory for Expansion Market files
        :return:
        | bool: Success or Failure
        | list: List of item files found
        """

        return True, FileManager.find_files(root_directory, ".json")
