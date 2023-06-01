from colorama import Fore, init as colorama_init
from standalone.validator import validate_json, validate_xml
from standalone.types_loader import load_profiles
from PyQt6.QtWidgets import QApplication, QMainWindow
from dayz_admin_tools.utilities.economy.Types import Types

from src.config import config
from src.forms import mainConfig

import sys

_profiles_directory = ""
_json_directory = ""
_xml_directory = ""
_market_dir = ""
_trader_dir = ""

_debug = True


def main():

    loaded_types = Types
    found_files = ()
    error_files = ()

    colorama_init()
    readconfig()
    for path in _json_directory:
        validate_json(path)

    for path in _xml_directory:
        validate_xml(path)

    if len(_profiles_directory) <= 0:
        print(Fore.RED+f"No DayZ Profile folder selected, exiting...")
    else:
        found_files, error_files, loaded_types = load_profiles(_profiles_directory)

#    for type_item in loaded_types.types():
#        print(type_item.filesource)

    return


def readconfig():
    """
    Opens and reads the application config, setting app variables
    :return:
    """
    global _profiles_directory
    global _json_directory
    global _xml_directory
    global _market_dir
    global _trader_dir

    app = QApplication(sys.argv)
    ConfigWindow = QMainWindow()
    ui = mainConfig.Ui_ConfigWindow()
    ui.setupUi(ConfigWindow)
    ConfigWindow.show()
    ret = app.exec()

    _profiles_directory, _market_dir, _trader_dir, _json_directory, _xml_directory = config.loadConfig()

    return


if __name__ == "__main__":
    main()
