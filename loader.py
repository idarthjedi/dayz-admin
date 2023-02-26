import os

from dayz_admin_tools.utilities.economy.Types import Types
from dayz_admin_tools.config import ROOT_DIR
from colorama import Fore, Back, Style, init as colorama_init
import argparse
import sys


def validate_profiles(profiles_directory: str):

    errors = []

    econ_types = Types()
    success, found_files = econ_types.load_type_files(profiles_directory)

    for f in found_files:
        success, error = econ_types.load_file(f)
        if not success:
            errors.append(error)

    if len(errors) > 0:
        for error_list in errors:
            for error in error_list:
                print(Fore.RED + error)
    else:
        print(Fore.GREEN+f"The following files were loaded, validated against a schema, and verified for unique values:{os.linesep}")
        [print(f"\t{Fore.GREEN}{x}") for x in found_files]


if __name__ == "__main__":

    colorama_init()
    parser = argparse.ArgumentParser(prog="loader.py",
                                     description="Loads all the types.xml from the DayZ profiles directory "\
                                                 "and validates them against a schema, and ensures there is "\
                                                 "only one instance of every class in all types.xml files.",
                                     )
    parser.add_argument("-d", "--dir",
                        help="Specify the root Profiles directory of DayZ to search for files to validate.",
                        action="store")

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
    validate_profiles(args.dir)