from colorama import Fore, Back, Style, init as colorama_init
from validator import validate_json, validate_xml
from loader import load_profiles
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from dayz_admin_tools.utilities.economy.Types import Types
from dayz_admin_tools.utilities.economy.Type import Type

import mainConfig
import sys
import os
import json

_profiles_directory = ""
_json_directory = ""
_xml_directory = ""

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

    if not os.path.exists('config/app-config.json'):
        # view in GUI
        pass

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainConfig.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ret = app.exec()

    with open('config/app-config.json') as config_file:
        try:
            config = json.load(config_file)
            _profiles_directory = config["properties"]["dayz-profile-dir"]
            _json_directory = config["properties"]["other_dirs"]["json"]
            _xml_directory = config["properties"]["other_dirs"]["xml"]
        except json.JSONDecodeError as error:
            print(Fore.RED + f"Cannot validate app-config.json")

    return


if __name__ == "__main__":
    main()
