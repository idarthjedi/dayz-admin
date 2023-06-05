import re
from dayz_admin_tools.utilities.files.fManager import FileManager


class Items(dict):
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

    def clean_file(self, input_list: list) -> list:

        # set up the regular expression to search for <VALUES>
        pattern = ".*?<(.*?)>"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        new_lines = []
        for line in input_list:
            # remove all the \t and \n from the start/end
            line = self._strip_codes(line)
            # if line has any <XYZ> that is not category (e.g. <CurrencyTrader>, <Currency>, <Trader>, etc. - skip it.
            result = regex.match(line)
            if result is not None:
                if result.group(0) != "<Category>":
                    # Some type of object identifier that is not a category
                    continue
                else:
                    # Set category name
                    line = self._remove_comments(line)
                    line = self._remove_notes(line)
                    new_lines.append(line)
            else:
                if line != "":
                    line = self._remove_comments(line)
                    line = self._remove_notes(line)
                    new_lines.append(line)

        return new_lines

    def _strip_codes(self, source: str) -> str:
        control_chars = ["\n", "\t"]
        # output = re.sub("\/\/.*", "", source).strip()
        for c in control_chars:
            source = source.strip(c)

        return source.strip()

    def _safe_filename(self, source: str) -> str:
        invalid = r'<>:"/\|?* ,'

        for char in invalid:
            source = source.replace(char, '_')

        return source

    def _remove_notes(self, string):
        pattern = r"(<<.*>>)"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        def _replacer(match):
            if match.group(1) is not None:
                return ""

        return regex.sub(_replacer, string)


    def _remove_comments(self, string):
        """
        Code taken from: https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files

        :param string:
        :return:
        """
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        # first group captures quoted strings (double or single)
        # second group captures comments (//single-line or /* multi-line */)
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        def _replacer(match):
            # if the 2nd group (capturing comments) is not None,
            # it means we have captured a non-quoted (real) comment string.
            if match.group(2) is not None:
                return ""  # so we will return empty to remove the comment
            else:  # otherwise, we will return the 1st group
                return match.group(1)  # captured quoted-string

        return regex.sub(_replacer, string)



