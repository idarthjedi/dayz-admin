from app.config import config
import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser as json_parser
from dayz_admin_tools.utilities.files.fManager import FileManager

import os
import sys
import argparse


def main(expansion_config_dir: str, primary_search_fragment: str, market_search_file: str, primary_search_section: str):
    """
    This function searches through
    :param expansion_config_dir: The main directory of the expansion mod
    :param primary_search_fragment: The fragment to search for in the airdrop settings and the associated market file
    :param market_search_file: The Market file to search
    :param primary_search_section: The section of the Airdrop file to search
    :return:
    """

    market_directory = os.path.join(expansion_config_dir, "Market")

    FileManager.backup(os.path.join(expansion_config_dir, "Settings", "AirdropSettings.json"))

    # load airdropsettings file
    with open(os.path.join(expansion_config_dir, "Settings", "AirdropSettings.json"), "r") as airdropsettings_file:
        airdrop_data = json.load(airdropsettings_file)

    classname_search = \
        json_parser.parse(f"$..Containers[?(@.Container == '{primary_search_section}')]" \
                          f".Loot[?(@.Name =~ '{primary_search_fragment}')]")

    drop_list = classname_search.find(airdrop_data)

    # first item
    # items_list[0].value['Name']
    # remove variants
    # items_list[0].value['Variants'].clear()

    # load up the provided file from market
    with open(os.path.join(market_directory, f"{market_search_file}")) as market_file:
        market_data = json.load(market_file)

    classname_search = \
        json_parser.parse(f"$..Items[?(@.ClassName =~ '{primary_search_fragment}')]")

    obj_list = classname_search.find(market_data)

    objs = []
    objs.append(obj_list[0].value['ClassName'])
    for obj in obj_list[0].value['Variants']:
        objs.append(obj)

    chance = 1 / len(objs)

    variants = []
    for vars in objs[1::]:
        variants.append({
                            "Name": f"{vars}",
                            "Attachments": [],
                            "Chance": chance
                        })

    # first item in Airdropsettings name is objs[0]
    drop_list[0].value['Name'] = objs[0]
    drop_list[0].value['Variants'] = variants

    with open(os.path.join(expansion_config_dir, "Settings", "AirdropSettings.json"), "w") as airdropsettings_file:
        json.dump(airdrop_data, airdropsettings_file, indent=2)


if __name__ == "__main__":

    section = "ExpansionAirdropContainer"

    parser = argparse.ArgumentParser(prog="airdrop_loader.py",
                                     description="Searches for objects in a specified market file, "\
                                     "adds those objects and all their variants to the airdropsettings, "\
                                     "given each variant equal spawn chances.",
                                     )
    parser.add_argument("-d", "--dir",
                        dest="dir",
                        help="Specify the root Expansion configuration directory to search for files to update.",
                        action="store")

    parser.add_argument("-i", "--item",
                        dest="item",
                        help="Specify the fragment of the item to search for, e.g. Diesel_TortillaBag",
                        action="store")

    parser.add_argument("-f", "--file",
                        dest="file",
                        help="Specify the specific Market file to examine",
                        action="store")

    parser.add_argument("-s", "--section",
                        dest="section",
                        choices=['d', 'default', 'm', 'medical', 'b', 'basebuilding', 'm', 'military'], default='d',
                        help="Identifies the section of the airdrop settings file",
                        action="store"
                        )

    if len(sys.argv) < 9:
        parser.print_help()
        exit()

    args = parser.parse_args()

    match args.section.lower():
        case "d" | "default":
            pass
        case "m" | "medical":
            section =+ "_Medical"
        case "b" | "basebuilding":
            section += "_Basebuilding"
        case "m" | "military":
            section += "_Military"
        case _:
            pass

    main(args.dir, args.item, args.file, section)
#    main(args.dir, "Diesel_TortillaBag", "joe_dfal_backpacks.json", section)
#    main(args.dir, "Diesel_DFAL", "joe_dfal.json", section)
#    main(args.dir, "Diesel_DFALZ", "joe_dfal.json", section)
#    main(args.dir, "Diesel_TacticalGloves", "joe_clothes.json", section)
#    main(args.dir, "Diesel_Suppressor", "joe_dfal_supp.json", section)
#    main(args.dir, "Diesel_HuntingOptic", "joe_dfal_opt.json", section)
#    main(args.dir, "Diesel_AttackVestPouches", "joe_clothes.json", section)
#    main(args.dir, "Diesel_GorkaJacket", "joe_clothes.json", section)
#    main(args.dir, "Diesel_GorkaPants", "joe_clothes.json", section)
#    main(args.dir, "Diesel_HikingLow", "joe_clothes.json", section)
#
#    main(args.dir, "Diesel_GhillieAtt", "joe_ghillies.json", section)
#    main(args.dir, "Diesel_GhillieHood", "joe_ghillies.json", section)
#    main(args.dir, "Diesel_Ghillie_Mossy", "joe_ghillies.json", section)
#    main(args.dir, "Diesel_Ghillie_Armband", "joe_ghillies.json", section)
#    main(args.dir, "Diesel_WarriorHelmet", "joe_clothes.json", section)
#