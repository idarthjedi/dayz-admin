import os

from lxml import etree
from dayz_admin_tools.config import ROOT_DIR
from dayz_admin_tools.utilities.economy.Type import Type


class Types:
    _types = {}

    def __init__(self):
        # load the XSD file
        xmlschema_doc = etree.parse(ROOT_DIR + "/dayz_admin_tools/utilities/economy/schemas/types.xsd")
        self._xmlschema = etree.XMLSchema(xmlschema_doc)
        pass

    def load_type_files(self, root_directory: str) -> tuple[bool, list]:
        """

        :param root_directory: Provide the root Profiles directory for the DayZ Server
        :return: bool: Success or Failure
                 list: List of type files loaded

        :exception individual type items must be unique across all types.xml files.
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

    def load_file(self, file: str) -> tuple[bool, str]:

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
            if obj_name in self._types:
                errors.append(f"Object {obj_name} already exists in types.xml with source: " \
                              f"{self._types[obj_name].filesource}.{os.linesep}\tError while parsing {file}{os.linesep}")

            self._types[obj_name] = Type(obj_name, file)

        return len(errors) == 0, errors

        # loop through each of the type in types
        # create a type class
        # add it to the dictionary
