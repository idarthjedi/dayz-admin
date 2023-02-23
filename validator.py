import sys

from dayz_admin_tools.utilities.files.json import JSONManager
import argparse


def validate_json(root_path: str):
    resp, files = JSONManager.validate_files(root_path)
    if resp:
        print(f"All JSON Files validated in path {root_path}\n")
    else:
        print(f"\nThe following files failed JSON validation:")
        [print(err) for err in files]


parser = argparse.ArgumentParser(prog="validator.py",
                                 description="Quick file validator for JSON and XML files",
                                 )
parser.add_argument("-t", "--type", choices=['JSON', 'XML'], default='XML',
                    help="Specify whether you want to validate JSON or XML(Default)",
                    action="store")
parser.add_argument("-d", "--dir",
                    help="Specify a directory to search for files to validate."\
                         "Multiple directories can be added using spaces between them",
                    action="append")

if len(sys.argv) < 2:
    parser.print_help()

args = parser.parse_args()

match args.type:
    case "JSON":
        for x in args.dir:
            validate_json(x)
    case "XML" | _:
        pass

