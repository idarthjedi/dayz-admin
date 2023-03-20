import json
import os


def loadConfig() -> tuple[str, list, list, list, list]:
    """

    :return: profile_directory, market_directory, trader_directory, json_directory, xml_directory
    """
    cur_dir = os.path.realpath(os.path.join(os.path.dirname(__file__)))
    # Load config file if it exists
    if not os.path.exists(f"{cur_dir}/app-config.json"):
        with open(f"{cur_dir}/src/app-config.latest.json", "r") as src:
            with open(f"{cur_dir}/app-config.json", "w") as dest:
                dest.write(src.read())

    if os.path.exists(f"{cur_dir}/app-config.json"):
        with open(f'{cur_dir}/app-config.json') as config_file:
            try:
                config = json.load(config_file)
                _config_version = float(config["config-version"])
                _profiles_directory = config["properties"]["dayz-profile-dir"]
                _json_directory = config["properties"]["other_dirs"]["json"]
                _xml_directory = config["properties"]["other_dirs"]["xml"]
                if _config_version <= 1.0:
                    _market_directory = ""
                    _trader_directory = ""
                else:
                    _market_directory = config["properties"]["market-dir"]
                    _trader_directory = config["properties"]["trader-dir"]
            except json.JSONDecodeError as error:
                raise "Cannot validate app-config.json"

    #TODO: Should change this into a dict object, before it grows too large!
    return _profiles_directory, _market_directory, _trader_directory, _json_directory, _xml_directory


def saveConfig(profileDir: str, market_dir: str, traders_dir: str, json_items: [], xml_items: []) -> bool:


    cur_dir = os.path.realpath(os.path.join(os.path.dirname(__file__)))

    data = {"config-version": 1.1}
    properties = {"dayz-profile-dir": profileDir,
                  "market-dir": market_dir,
                  "trader-dir": traders_dir
                  }

    other_dirs, json_dirs, xml_dirs = {}, {}, {}

    other_dirs["json"] = json_items
    other_dirs["xml"] = xml_items
    properties["other_dirs"] = other_dirs
    data["properties"] = properties

    with open(f"{cur_dir}/app-config.json", mode="w") as config_file:
        config_file.write(json.dumps(data))

    return True
