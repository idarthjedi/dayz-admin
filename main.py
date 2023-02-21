from dayz_admin_tools.utilities.files.json import JSONManager
from dayz_admin_tools.utilities.files.xml import XMLManager


def validate_files():
    file1 = JSONManager("local.json")
    file2 = XMLManager("local.xml")
    print(file1.validate())
    print(file2.validate())


validate_files()
