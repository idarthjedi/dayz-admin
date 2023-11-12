import json
import math
import os

import dayz_admin_tools.utilities.traders.expansion.Items
from dayz_admin_tools.config import _DEBUG

from dayz_admin_tools.utilities.traders.expansion.Item import Item as market_item
from dayz_admin_tools.utilities.traders.traderplus.Vehicle_Parts import Vehicle_Parts as trader_items


from colorama import Fore, Back, Style, init as colorama_init
from dayz_admin_tools.utilities.files.fManager import FileManager
import argparse
import sys
import re


def main(filename: str, default_price: int = 500, multiplier: float = 1.0):

    trader_items_object = trader_items(filename)
    market_file = dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()

    market_collection = market_file["Items"]
    input_filename = FileManager.return_filename(filename, True)
    dir_basename = FileManager.return_dirname(filename)
    # set up the regular expression to search for <VALUES>

    new_lines = []
    # right now there is an assumption that the traderplus file is correctly formatted
    with open(filename) as tp_file:
        new_lines = trader_items_object.clean_file(tp_file.readlines())

    market_file["Items"].clear()

    for vehicle in new_lines:
        created_item = market_item.create_new(vehicle)
        price = default_price
        created_item["MaxPriceThreshold"] = math.floor(float(price) * multiplier)
        created_item["MinPriceThreshold"] = math.floor(float(price) * multiplier)
        for attachment in new_lines[vehicle]:
            created_item["SpawnAttachments"].append(attachment)

        market_collection.append(created_item)

    market_file["DisplayName"] = os.path.basename(input_filename[0]).replace("_Vehicle")
    output_filename = os.path.join(dir_basename, f"expansion_{os.path.basename(input_filename[0])}.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(market_file, output_file, indent=2)

def _strip_codes(source: str) -> str:
    control_chars = ["\n", "\t"]
    # output = re.sub("\/\/.*", "", source).strip()
    for c in control_chars:
        source = source.strip(c)

    return source.strip()


def _safe_filename(source: str) -> str:
    invalid = r'<>:"/\|?* ,'

    for char in invalid:
        source = source.replace(char, '_')

    return source


if __name__ == "__main__":
    colorama_init()
    parser = argparse.ArgumentParser(prog="traderplusparts_to_vehicle_expansion.py",
                                     description="Takes as input the name of a traderplus Vehicle Parts file, and will output an "\
                                                 "Expansion trader file of the same name all the individual parts "\
                                                "created as SpawnAttachments."
                                     )
    parser.add_argument("-f", "--file",
                        help="Specify the TraderPlus file name to convert.",
                        action="store",
                        required=True)

    parser.add_argument("-m", "--multiplier", type=float,
                        help="Specify the optional price multiplier for the TraderPlus to Expansion conversion",
                        action="store",
                        required=False)

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
    if args.multiplier:
        main(args.file, multiplier=args.multiplier)
    else:
        main(args.file)


