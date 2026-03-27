import argparse
import json
import math
import os
import sys

from colorama import init as colorama_init

import dayz_admin_tools.utilities.traders.expansion.Items
from dayz_admin_tools.config import _DEBUG
from dayz_admin_tools.defaults import DEFAULT_PRICE, GENERIC_VEHICLE_PARTS
from dayz_admin_tools.utilities.files.fManager import FileManager
from dayz_admin_tools.utilities.text import safe_filename, strip_codes
from dayz_admin_tools.utilities.traders.expansion.Item import Item as market_item
from dayz_admin_tools.utilities.traders.traderplus.Vehicle_Parts import (
    Vehicle_Parts as trader_items,
)


def main(filename: str, default_price: int = DEFAULT_PRICE, multiplier: float = 1.0):

    unique_parts_names = set()

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
        price = math.floor(default_price * multiplier)
        created_item["MaxPriceThreshold"] = price
        created_item["MinPriceThreshold"] = price
        for attachment in new_lines[vehicle]:

            created_item["SpawnAttachments"].append(attachment)
            if attachment not in unique_parts_names:
                if attachment not in GENERIC_VEHICLE_PARTS:
                    parts_created_item = market_item.create_new(attachment)
                    parts_created_item["MaxPriceThreshold"] = price
                    parts_created_item["MinPriceThreshold"] = price
                    parts_collection.append(parts_created_item)

                    unique_parts_names.add(attachment)

        market_collection.append(created_item)

    # create Vehicle_Parts file
    parts_file["DisplayName"] = os.path.basename(f"{input_filename[0]} Parts")
    output_filename = os.path.join(
        dir_basename, f"expansion_{os.path.basename(input_filename[0])}.json"
    )
    with open(output_filename, mode="w") as output_file:
        json.dump(parts_file, output_file, indent=2)

    market_file["DisplayName"] = os.path.basename(input_filename[0]).replace(
        "_Vehicle_parts", ""
    )
    output_filename = os.path.join(
        dir_basename,
        f"expansion_{os.path.basename(input_filename[0]).replace('_Vehicle_parts', '')}.json",
    )
    with open(output_filename, mode="w") as output_file:
        json.dump(market_file, output_file, indent=2)

    # create generic vehicle parts file
    # Adding these in by hand, b/c they seem to always be in common - will have to tweak if that isn't the case
    generic_market_file = (
        dayz_admin_tools.utilities.traders.expansion.Items.Items.file_header()
    )
    generic_collection = generic_market_file["Items"]

    generic_price = math.floor(default_price * multiplier)
    for part in GENERIC_VEHICLE_PARTS:
        created_item = market_item.create_new(part)
        created_item["MaxPriceThreshold"] = generic_price
        created_item["MinPriceThreshold"] = generic_price
        generic_collection.append(created_item)

    generic_market_file["DisplayName"] = "Generic Vehicle Parts"
    output_filename = os.path.join(dir_basename, "Generic_Vehicle_Parts.json")
    with open(output_filename, mode="w") as output_file:
        json.dump(generic_market_file, output_file, indent=2)

    # create the Vehicle Parts file

    pass


if __name__ == "__main__":
    colorama_init()
    parser = argparse.ArgumentParser(
        prog="traderplusparts_to_vehicle_expansion.py",
        description="Takes as input the name of a traderplus Vehicle Parts file, and will output an "
        "Expansion trader file of the same name all the individual parts "
        "created as SpawnAttachments.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Specify the TraderPlus file name to convert.",
        action="store",
        required=True,
    )

    parser.add_argument(
        "-m",
        "--multiplier",
        type=float,
        help="Specify the optional price multiplier for the TraderPlus to Expansion conversion",
        action="store",
        required=False,
    )

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
    if args.multiplier:
        main(args.file, multiplier=args.multiplier)
    else:
        main(args.file)
