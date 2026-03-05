import re

from dayz_admin_tools.utilities.files.fManager import FileManager
from dayz_admin_tools.utilities.text import remove_comments, remove_notes, strip_codes


class Vehicle_Parts(dict):
    # _types = {}

    _filename = ""

    def __init__(self, filename):
        self._filename = filename
        super().__init__()

    def load_items(self, file: str) -> tuple[bool, list]:
        """
        Loads individual items across all market files, will record errors if duplicates are found to already exist.
        :param file: name of the file to load into the types collection
        :return: True for no errors, False for errors, and a list of duplicate items
        """

        input_filename = FileManager.return_filename(self._filename, True)
        dir_basename = FileManager.return_dirname(self._filename)

        new_lines = []
        # right now there is an assumption that the traderplus file is correctly formatted
        with open(self._filename) as tp_file:
            new_lines = self.clean_file(tp_file.readlines())

        pass

    def clean_file(self, input_list: list) -> dict:

        # set up the regular expression to search for <VALUES>
        pattern = ".*?<(.*?)>"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        new_lines = {}
        vehicle_name = ""
        for line in input_list:
            # remove all the \t and \n from the start/end
            line = strip_codes(line)
            # if line has any <XYZ> that is not category (e.g. <CurrencyTrader>, <Currency>, <Trader>, etc. - skip it.
            result = regex.match(line)
            if result is not None:
                if result.group(0) != "<VehicleParts>":
                    # Some type of object identifier that is not a category
                    continue
                else:
                    # Set category name
                    line = remove_comments(line)
                    line = remove_notes(line)
                    # new_lines.append(line.replace("<VehicleParts> ", ""))
                    vehicle_name = strip_codes(
                        line.replace("<VehicleParts>", "").strip()
                    )
                    new_lines[vehicle_name] = []

            else:
                if line != "":
                    line = remove_comments(line)
                    line = remove_notes(line)
                    new_lines[vehicle_name].append(line)

        return new_lines

