from dayz_admin_tools.utilities.files.json import JSONManager
from dayz_admin_tools.utilities.files.xml import XMLManager
from colorama import Fore, Back, Style, init as colorama_init
import sys
import os
import argparse

tab_char = "\t"


def validate_json(root_path: str):
    resp, count, files = JSONManager.validate_files(root_path)

    print(Fore.GREEN + f"{count} JSON Files validated{os.linesep}{tab_char}path{root_path}{os.linesep}")
    if not resp:
        print(Fore.RED + f"The following files failed JSON validation:")
        [print(f"{tab_char}{err}") for err in files]
        print(os.linesep)


def validate_xml(root_path: str):
    resp, count, files = XMLManager.validate_files(root_path)

    print(Fore.GREEN + f"{count} XML Files validated{os.linesep}{tab_char}path{root_path}{os.linesep}")
    if not resp:
        print(Fore.RED + f"The following files failed XML validation:")
        [print(f"{tab_char}{err}") for err in files]
        print(os.linesep)


def main():
    parser = argparse.ArgumentParser(prog="validator.py",
                                     description="Quick file validator for JSON and XML files",
                                     )
    parser.add_argument("-t", "--type", choices=['JSON', 'XML', 'BOTH'], default='BOTH',
                        help="Specify whether you want to validate JSON or XML(Default)",
                        action="store")
    parser.add_argument("-d", "--dir",
                        help="Specify a directory to search for files to validate."\
                             "Multiple directories can be added using spaces between them",
                        action="append")

    if len(sys.argv) < 5:
        parser.print_help()
        exit()

    args = parser.parse_args()

    match args.type:
        case "JSON":
            for x in args.dir:
                validate_json(x)

        case "XML":
            for x in args.dir:
                validate_xml(x)

        case "BOTH" | _:
            for x in args.dir:
                validate_json(x)

            for x in args.dir:
                validate_xml(x)


if __name__ == "__main__":
    colorama_init()
    main()
