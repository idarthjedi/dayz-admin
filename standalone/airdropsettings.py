from app.config import config
import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser as json_parser

import os


def main(primary_search_fragment: str, market_search_file: str, primary_search_section: str):
    """

    :param primary_search_fragment: The fragment to search for in the airdrop settings and the associated market file
    :param market_search_file: The Market file to search
    :param primary_search_section: The section of the Airdrop file to search
    :return:
    """
    profile_directory, market_directory, trader_directory, json_directory, xml_directory = config.loadConfig()

    # cheating right now, b/c I'm lazy...
    expansion_config_dir = os.path.commonprefix([market_directory, trader_directory])

    # load airdropsettings file
    with open(os.path.join(expansion_config_dir, "Settings", "AirdropSettings.json"), "r") as airdropsettings_file:
        airdrop_data = json.load(airdropsettings_file)

    with open(os.path.join(expansion_config_dir, "Settings", "AirdropSettings.bak.json"), "w") as airdropsettings_file:
       json.dump(airdrop_data, airdropsettings_file, indent=2)


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
    main("Diesel_TortillaBag", "Backpacks.json", "ExpansionAirdropContainer_Military")
    main("Diesel_DFAL", "joe_dfal.json", "ExpansionAirdropContainer_Military")
    main("Diesel_DFALZ", "joe_dfal.json", "ExpansionAirdropContainer_Military")
    main("Diesel_TracticalGloves", "joe_clothes.json", "ExpansionAirdropContainer_Military")
    main("Diesel_Suppressor", "joe_dfal_supp.json", "ExpansionAirdropContainer_Military")
    main("Diesel_HuntingOptic", "joe_dfal_opt.json", "ExpansionAirdropContainer_Military")
    main("Diesel_AttackVestPouches", "joe_clothes.json", "ExpansionAirdropContainer_Military")
    main("Diesel_GorkaJacket", "joe_clothes.json", "ExpansionAirdropContainer_Military")
    main("Diesel_GorkaPants", "joe_clothes.json", "ExpansionAirdropContainer_Military")
    main("Diesel_HikingLow", "joe_clothes.json", "ExpansionAirdropContainer_Military")


