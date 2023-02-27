import os

from lxml import etree
from dayz_admin_tools.config import ROOT_DIR
from dayz_admin_tools.utilities.economy.Type import Type
from colorama import Fore, Back, Style


class Types(dict):
    # _types = {}

    def __init__(self):
        # load the XSD file
        xmlschema_doc = etree.parse(ROOT_DIR + "/dayz_admin_tools/utilities/economy/schemas/types.xsd")
        self._xmlschema = etree.XMLSchema(xmlschema_doc)
        super().__init__()

    @staticmethod
    def find_type_files(root_directory: str) -> tuple[bool, list]:
        """

        :param root_directory: Provide the root Profiles directory for the DayZ Server
        :return:
        | bool: Success or Failure
        | list: List of type files found
        """

        list_files = []

        # first validate the existance of db\types.xml
        if os.path.isfile(os.path.join(root_directory, "db/types.xml")):
            list_files.append(os.path.join(root_directory, "db/types.xml"))
        else:
            raise Exception(f"/db/types.xml not found in path: {root_directory}")

        cfge_file = etree.parse(os.path.join(root_directory, "cfgeconomycore.xml"))

        folders = cfge_file.xpath("//@folder")
        for each_folder in folders:
            # //*[@folder='expansion_ce']/file[@type='types']
            include_files = cfge_file.xpath(f"//*[@folder='{each_folder}']/file[@type='types']")
            for each_type_file in include_files:
                list_files.append(os.path.join(root_directory, each_folder, each_type_file.attrib["name"]))

        return True, list_files

    def load_types(self, file: str) -> tuple[bool, list]:
        """
        Loads individual types across all type files, will record errors if duplicates are found to already exist.
        :param file: name of the file to load into the types collection
        :return: True for no errors, False for errors, and a list of duplicate items
        """
        errors = []
        xml_doc = etree.parse(file)
        try:
            self._xmlschema.assertValid(xml_doc)
        except etree.DocumentInvalid as error:
            errors.append(error.args[0] + f" in file: {file}{os.linesep}")
            # The document failed Schema Validation, move onto the next document
            return False, errors

        # xml turned out to be valid per schema, loop through each of the type in types and create an type object
        all_types = xml_doc.xpath("//types/type")
        for each_type in all_types:
            obj_name = each_type.attrib['name']
            if obj_name in self:
                errors.append(f"Object {obj_name} duplications:{os.linesep}"\
                              f"\t{Fore.GREEN}Winner: {self[obj_name].filesource}{os.linesep}"\
                              f"\t{Fore.RED}Loser: {file}.")

            else:
                # Only append if there wasn't a duplicate already
                self[obj_name] = Type(obj_name, file)

        return len(errors) == 0, errors

  #  def types(self) -> Type:
  #      for type_instance in self.values():
  #          yield type_instance
