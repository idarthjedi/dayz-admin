import json
import os


def loadConfig() -> tuple[str, list, list, list, list]:
    # Load config file if it exists
    if not os.path.exists("config/app-config.json"):
        with open("config/src/app-config.latest.json", "r") as src:
            with open("config/app-config.json", "w") as dest:
                dest.write(src.read())

    if os.path.exists("config/app-config.json"):
        with open('config/app-config.json') as config_file:
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

    with open("config/app-config.json", mode="w") as config_file:
        config_file.write(json.dumps(data))

    return True
