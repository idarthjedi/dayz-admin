import json
import math
import os
from dayz_admin_tools.config import _DEBUG

from dayz_admin_tools.utilities.traders.expansion.Item import Item as market_item
from colorama import Fore, Back, Style, init as colorama_init
from dayz_admin_tools.utilities.files.fManager import FileManager
import argparse
import sys
import re


def main(filename: str, default_price: int = 500, multiplier: float = 1.0):

    market_file = {
        "m_Version": 12,
        "DisplayName": "",
        "Icon": "Deliver",
        "Color": "FBFCFEFF",
        "IsExchange": 0,
        "InitStockPercent": 75.0,
        "Items": []
    }

    market_collection = market_file["Items"]
    input_filename = FileManager.return_filename(filename, True)
    dir_basename = FileManager.return_dirname(filename)
    # set up the regular expression to search for <VALUES>
    pattern = ".*?<(.*?)>"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    new_lines = []
    # right now there is an assumption that the traderplus file is correctly formatted
    with open(filename) as tp_file:
        current_category = ""
        tp_clean_data = tp_file.readlines()

        for line in tp_clean_data:
            # remove all the \t and \n from the start/end
            line = _strip_codes(line)
            # if line has any <XYZ> that is not category (e.g. <CurrencyTrader>, <Currency>, <Trader>, etc. - skip it.
            result = regex.match(line)
            if result is not None:
                if result.group(0) != "<Category>":
                    # Some type of object identifier that is not a category
                    continue
                else:
                    # Set category name
                    line = _remove_comments(line)
                    line = _remove_notes(line)
                    new_lines.append(line)
            else:
                if line != "":
                    line = _remove_comments(line)
                    line = _remove_notes(line)
                    new_lines.append(line)

    tp_data = '\n'.join(new_lines)

    tp_categories = tp_data.split("<Category>")
    for categories in tp_categories:

        if categories == "":
            continue

        market_file["Items"].clear()
        items_list = categories.splitlines()
        if len(items_list) > 1:

            # strip comments if they exist
            category = items_list.pop(0)

            category = _strip_codes(category)
            category_filename = _safe_filename(category)

            if _DEBUG:
                print(f"Categories: {category} ")
            for items in items_list:
                if len(items) != 0:
                    items_collection = items.split(",")
                    item_name = items_collection.pop(0).strip()
                    if len(item_name) != 0:
                        if _DEBUG:
                            print(f"Item name: {item_name}")

                        created_item = market_item.create_new(item_name)
                        price = default_price

                        # some files are malformed and don't have prices
                        if len(items_collection) >= 3:
                            tmp_price = int(_strip_codes(items_collection[1]))
                            tmp_price2 = int(_strip_codes(items_collection[2]))
                            if tmp_price == -1:
                                price = tmp_price2
                            else:
                                price = tmp_price

                        created_item["MaxPriceThreshold"] = math.floor(float(price) * multiplier)
                        created_item["MinPriceThreshold"] = math.floor(float(price) * multiplier)
                        market_collection.append(created_item)

                        for item_prop in items_collection:
                            if _DEBUG:
                                print(f"Item Property: {_strip_codes(item_prop)}")

            market_file["DisplayName"] = category

            output_filename = os.path.join(dir_basename, f"{input_filename[0]}_{category_filename}.json")
            with open(output_filename, mode="w") as output_file:
                json.dump(market_file, output_file, indent=2)

            if _DEBUG:
                print(json.dumps(market_file, indent=2))


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


def _remove_notes(string):
    pattern = r"(<<.*>>)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(1) is not None:
            return ""

    return regex.sub(_replacer, string)


def _remove_comments(string):
    """
    Code taken from: https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files

    :param string:
    :return:
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)


if __name__ == "__main__":
    colorama_init()
    parser = argparse.ArgumentParser(prog="traderplus_to_expansion.py",
                                     description="Takes as input the name of a traderplus file, and will output an "\
                                                 "Expansion trader file of the same name with category extensions (e.g.) "\
                                                 "FILE=geb_trader, output=geb_trader_fish.json, geb_trader_fishmeat.json, etc. "\
                                                 "Code optionally takes a multiplier (float) to apply against the priceses listed in "\
                                                "the traderplus file e.g. 1.5 multiper will make the prices 1.5 times higher than "\
                                                "in the original traderplus file."
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


