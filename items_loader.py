import os

from dayz_admin_tools.utilities.traders.expansion.Items import Items
from dayz_admin_tools.config import ROOT_DIR
from colorama import Fore, Back, Style, init as colorama_init
import argparse
import sys


def load_items(market_directory: str) -> tuple[list, list, Items]:
    """

    :param market_directory: Market Directory to load all the Type JSON Files

    :return:
        list->found_files: All the Item files that were found in the directory
        list->errors: All the files that had errors
        Types: Collection of all the Items loaded across all the files
    """
    errors = []

    market_items = Items()
    success, found_files = Items.find_item_files(market_directory)

    for f in found_files:
        success, error = market_items.load_items(f)
        if not success:
            errors.append(error)

    print(Fore.GREEN+f"The following files were loaded, validated against a schema, and checked for unique values:{os.linesep}")
    [print(f"\t{Fore.GREEN}{x}") for x in found_files]
    print(f"{os.linesep}")

    if len(errors) > 0:
        for error_list in errors:
            for error in error_list:
                print(Fore.RED + error)

    return found_files, errors, market_items


if __name__ == "__main__":

    colorama_init()
    parser = argparse.ArgumentParser(prog="items_loader.py",
                                     description="Loads all the Market Items JSON files from the Markets directory "\
                                                 "and validates them against a schema, and ensures there is "\
                                                 "only one instance of every class in all Market files.",
                                     )
    parser.add_argument("-d", "--dir",
                        help="Specify the Markets directory of Expansion Market folder to search for files to validate.",
                        action="store")

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
    load_items(args.dir)
