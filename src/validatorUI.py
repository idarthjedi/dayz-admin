import sys
from dataclasses import dataclass, field

from colorama import Fore
from colorama import init as colorama_init
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.config import config
from src.forms import mainConfig
from standalone.types_loader import load_profiles
from standalone.validator import validate_json, validate_xml


@dataclass
class AppConfig:
    profiles_directory: str = ""
    json_directory: list = field(default_factory=list)
    xml_directory: list = field(default_factory=list)
    market_dir: str = ""
    trader_dir: str = ""


def read_config() -> AppConfig:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    config_window = QMainWindow()
    ui = mainConfig.Ui_ConfigWindow()
    ui.setupUi(config_window)
    config_window.show()
    app.exec()

    profiles, market, trader, json_dirs, xml_dirs = config.loadConfig()
    return AppConfig(
        profiles_directory=profiles,
        json_directory=json_dirs,
        xml_directory=xml_dirs,
        market_dir=market,
        trader_dir=trader,
    )


def main():
    colorama_init()
    cfg = read_config()

    for path in cfg.json_directory:
        validate_json(path)

    for path in cfg.xml_directory:
        validate_xml(path)

    if not cfg.profiles_directory:
        print(Fore.RED + "No DayZ Profile folder selected, exiting...")
    else:
        load_profiles(cfg.profiles_directory)


if __name__ == "__main__":
    main()
