import os

from dayz_admin_tools.utilities.economy.Types import Types
from dayz_admin_tools.config import ROOT_DIR
from colorama import Fore, Back, Style, init as colorama_init
import argparse
import sys


def load_profiles(profiles_directory: str) -> tuple[list, list, Types]:
    """

    :param profiles_directory: DayZ Server Profile Directory to load all the Type XML Files

    :return:
        list->found_files: All the type files that were found in the directory<br/>
        list->errors: All the files that had errors
        Types: Collection of all the types loaded across all the files
    """
    errors = []

    econ_types = Types()
    success, found_files = Types.find_type_files(profiles_directory)
    # success, found_files = econ_types.load_type_files(profiles_directory)

    for f in found_files:
        success, error = econ_types.load_types(f)
        if not success:
            errors.append(error)

    print(Fore.GREEN+f"The following files were loaded, validated against a schema, and checked for unique values:{os.linesep}")
    [print(f"\t{Fore.GREEN}{x}") for x in found_files]
    print(f"{os.linesep}")

    if len(errors) > 0:
        for error_list in errors:
            for error in error_list:
                print(Fore.RED + error)

    return found_files, errors, econ_types


if __name__ == "__main__":

    colorama_init()
    parser = argparse.ArgumentParser(prog="types_loader.py",
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
    load_profiles(args.dir)
