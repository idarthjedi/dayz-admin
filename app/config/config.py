import json
import os


def loadConfig() -> tuple[str, list, list]:
    # Load config file if it exists
    if not os.path.exists("config/app-config.json"):
        with open("config/src/app-config.latest.json", "r") as src:
            with open("config/app-config.json", "w") as dest:
                dest.write(src.read())

    if os.path.exists("config/app-config.json"):
        with open('config/app-config.json') as config_file:
            try:
                config = json.load(config_file)
                _profiles_directory = config["properties"]["dayz-profile-dir"]
                _json_directory = config["properties"]["other_dirs"]["json"]
                _xml_directory = config["properties"]["other_dirs"]["xml"]
            except json.JSONDecodeError as error:
                raise "Cannot validate app-config.json"

    return _profiles_directory, _json_directory, _xml_directory


def saveConfig(profileDir: str, json_items: [], xml_items: []) -> bool:

    data = {"config-version": "1.0"}
    properties = {"dayz-profile-dir": profileDir}

    other_dirs, json_dirs, xml_dirs = {}, {}, {}

    other_dirs["json"] = json_items
    other_dirs["xml"] = xml_items
    properties["other_dirs"] = other_dirs
    data["properties"] = properties

    with open("config/app-config.json", mode="w") as config_file:
        config_file.write(json.dumps(data))

    return True
