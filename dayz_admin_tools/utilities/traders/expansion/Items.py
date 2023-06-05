import os
import json
import jsonschema.exceptions

from dayz_admin_tools.config import ROOT_DIR
from jsonschema import validate as json_validate
from dayz_admin_tools.utilities.files.fManager import FileManager
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser as json_parser

from dayz_admin_tools.utilities.traders.expansion.Item import Item
from colorama import Fore, Back, Style


class Items(dict):

    def __init__(self):
        # load the XSD file
        with open(ROOT_DIR + "/dayz_admin_tools/utilities/traders/expansion/schemas/items.schema.json", "r") as schema_doc:
            self._jsonschema = json.loads(schema_doc.read())

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

    def load_items(self, file: str) -> tuple[bool, list]:
        """
        Loads individual items across all market files, will record errors if duplicates are found to already exist.
        :param file: name of the file to load into the types collection
        :return: True for no errors, False for errors, and a list of duplicate items
        """
        errors = []
        with open(file, "r") as json_file:
            json_doc = json.load(json_file)

        try:
            json_validate(json_doc, self._jsonschema)
        except Exception as error:
            errors.append(error.args[0] + f" in file: {file}{os.linesep}")
            # The document failed Schema Validation, move onto the next document
            return False, errors

        classname_search = json_parser.parse('$..Items..ClassName')

        items_list = classname_search.find(json_doc)
        if len(items_list) <= 0:
            errors.append(f"{Fore.RED}{file} contains no Items!")
            return

        for market_item in items_list:
            if market_item.value in self:
                errors.append(f"Object {market_item.value} duplications:{os.linesep}"\
                              f"\t{Fore.GREEN}Winner: {self[market_item.value].filesource}{os.linesep}"\
                              f"\t{Fore.RED}Loser: {file}.")
            else:
                parent = self[market_item.value] = Item(market_item.value, file)
                # check for Variants
                variants_search = json_parser.parse(
                    f"$.Items[?(@.ClassName=='{market_item.value}')].Variants")
                variants_list = variants_search.find(json_doc)
                if len(variants_list[0].value) > 0:
                    # no variants
                    for variant in variants_list[0].value:
                        if variant in self:
                            errors.append(f"Object {variant} variant listed with duplications:{os.linesep}" \
                                          f"\t{Fore.GREEN}Winner: {self[variant].filesource}{os.linesep}" \
                                          f"\t{Fore.RED}Loser: {file}.")
                        else:
                            self[variant] = Item(variant, file, parent)

        # JSON turned out to be valid per schema, loop through each of the Items and create an Item object
        
#        # xml turned out to be valid per schema, loop through each of the type in types and create an type object
#        all_types = xml_doc.xpath("//types/type")
#        for each_type in all_types:
#            obj_name = each_type.attrib['name']
#            if obj_name in self:
#                errors.append(f"Object {obj_name} duplications:{os.linesep}"\
#                              f"\t{Fore.GREEN}Winner: {self[obj_name].filesource}{os.linesep}"\
#                              f"\t{Fore.RED}Loser: {file}.")
#
#            else:
#                # Only append if there wasn't a duplicate already
#                self[obj_name] = Type(obj_name, file)
#
        return len(errors) == 0, errors

    @staticmethod
    def file_header() -> dict:

        return {
            "m_Version": 12,
            "DisplayName": "",
            "Icon": "Deliver",
            "Color": "FBFCFEFF",
            "IsExchange": 0,
            "InitStockPercent": 25.0,
            "Items": []
        }
