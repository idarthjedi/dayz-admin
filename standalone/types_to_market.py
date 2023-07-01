from dayz_admin_tools.utilities.files.fManager import FileManager
from dayz_admin_tools.utilities.economy.Types import Types
import dayz_admin_tools.utilities.traders.expansion.Items
from dayz_admin_tools.utilities.traders.expansion.Item import Item as market_item
import json
from colorama import Fore, Back, Style, init as colorama_init
import sys
import os
import argparse


def convert_types(types_file: str, default_price: int, category: str) -> bool:

    market_file = dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()

    market_collection = market_file["Items"]
    input_filename = FileManager.return_filename(types_file, True)
    dir_basename = FileManager.return_dirname(types_file)
    errors = []

    econ_types = Types()

    success, error = econ_types.load_types(types_file)
    if not success:
        errors.append(error)
        return False

    for type_item in econ_types:

        created_item = market_item.create_new(type_item)
        price = default_price

        created_item["MaxPriceThreshold"] = default_price
        created_item["MinPriceThreshold"] = default_price
        market_collection.append(created_item)

    market_file["DisplayName"] = category

    output_filename = os.path.join(dir_basename, f"{input_filename[0]}_{category}.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(market_file, output_file, indent=2)

    return True


if __name__ == "__main__":

    colorama_init()
    parser = argparse.ArgumentParser(prog="types_to_market.py",
                                     description="Loads the type file specified, and converts it into "\
                                                 "a market file, using pre-defined defaults. "\
                                     )
    parser.add_argument("-f", "--file",
                        help="Specify the types file to convert.",
                        action="store")

    parser.add_argument("-p", "--price",
                        help="Specify the default price for the imported items.",
                        action="store")

    parser.add_argument("-c", "--category",
                        help="Specify the Category name for the imported items.",
                        action="store")

    if len(sys.argv) < 7:
        parser.print_help()
        exit()

    args = parser.parse_args()
    convert_types(args.file, args.price, args.category)