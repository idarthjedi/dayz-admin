import os
import sys
from pathlib import Path

if sys.argv:
    sys.path.insert(0, str(Path(sys.argv[0]).resolve().parent.parent))

import argparse

from colorama import Back, Fore, Style
from colorama import init as colorama_init

from dayz_admin_tools.config import ROOT_DIR
from dayz_admin_tools.utilities.economy.Types import Types

if __name__ == "__main__":

    colorama_init()
    parser = argparse.ArgumentParser(
        prog=f"{sys.argv[0]}",
        description="Loads two types files and compares all the entries in the types file",
    )
    parser.add_argument(
        "-f1",
        "--file1",
        help="Specify the first types file to compare.",
        action="store",
        required=True,
        metavar="file1",
    )

    parser.add_argument(
        "-f2",
        "--file2",
        help="Specify the second types file to compare.",
        action="store",
        required=True,
        metavar="file2",
    )

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
#    load_items(args.dir, args.ignore_variants)
