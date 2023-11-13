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

    # list of generic parts to not include in the main parts file, but to put in a generic parts file
    generic_vehicle_parts = ["SparkPlug", "CarBattery", "CarRadiator","HeadlightH7", "TruckBattery"]
    unique_parts_names = []

    trader_items_object = trader_items(filename)
    market_file = dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()
    parts_file = dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()

    parts_collection = parts_file["Items"]
    market_collection = market_file["Items"]

    input_filename = FileManager.return_filename(filename, True)
    dir_basename = FileManager.return_dirname(filename)
    # set up the regular expression to search for <VALUES>

    new_lines = []
    # right now there is an assumption that the traderplus file is correctly formatted
    with open(filename) as tp_file:
        new_lines = trader_items_object.clean_file(tp_file.readlines())

    market_file["Items"].clear()

    # create the main vehicle file
    for vehicle in new_lines:
        created_item = market_item.create_new(vehicle)
        price = default_price
        created_item["MaxPriceThreshold"] = math.floor(float(price) * multiplier)
        created_item["MinPriceThreshold"] = math.floor(float(price) * multiplier)
        for attachment in new_lines[vehicle]:

            created_item["SpawnAttachments"].append(attachment)
            if attachment not in unique_parts_names:
                if attachment not in generic_vehicle_parts:
                    parts_created_item = market_item.create_new(attachment)
                    price = default_price
                    parts_created_item["MaxPriceThreshold"] = math.floor(float(price) * multiplier)
                    parts_created_item["MinPriceThreshold"] = math.floor(float(price) * multiplier)
                    parts_collection.append(parts_created_item)

                    unique_parts_names.append(attachment)

        market_collection.append(created_item)

    # create Vehicle_Parts file
    parts_file["DisplayName"] = os.path.basename(f"{input_filename[0]} Parts")
    output_filename = os.path.join(dir_basename, f"expansion_{os.path.basename(input_filename[0])}.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(parts_file, output_file, indent=2)

    market_file["DisplayName"] = os.path.basename(input_filename[0]).replace("_Vehicle_parts", "")
    output_filename = os.path.join(dir_basename, f"expansion_{os.path.basename(input_filename[0]).replace('_Vehicle_parts', '')}.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(market_file, output_file, indent=2)

    # create generic vehicle parts file
    # Adding these in by hand, b/c they seem to always be in common - will have to tweak if that isn't the case
    generic_market_file = dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()
    generic_collection = generic_market_file["Items"]

    for part in generic_vehicle_parts:
        created_item = market_item.create_new(part)
        price = default_price
        created_item["MaxPriceThreshold"] = math.floor(float(price) * multiplier)
        created_item["MinPriceThreshold"] = math.floor(float(price) * multiplier)
        generic_collection.append(created_item)

    generic_market_file["DisplayName"] = "Generic Vehicle Parts"
    output_filename = os.path.join(dir_basename, "Generic_Vehicle_Parts.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(generic_market_file, output_file, indent=2)


    # create the Vehicle Parts file

    pass


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


