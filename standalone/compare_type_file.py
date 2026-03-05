import os
import sys
from pathlib import Path

if sys.argv:
    sys.path.insert(0, str(Path(sys.argv[0]).resolve().parent.parent))

import argparse

from colorama import Fore
from colorama import init as colorama_init

from dayz_admin_tools.utilities.economy.Types import Types


def compare_types(file1: str, file2: str) -> None:
    types1 = Types()
    types2 = Types()

    success1, errors1 = types1.load_types(file1)
    success2, errors2 = types2.load_types(file2)

    if not success1:
        print(Fore.RED + f"Failed to load {file1}:")
        for err in errors1:
            print(f"\t{err}")
        return

    if not success2:
        print(Fore.RED + f"Failed to load {file2}:")
        for err in errors2:
            print(f"\t{err}")
        return

    set1 = set(types1.keys())
    set2 = set(types2.keys())

    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1
    in_both = set1 & set2

    print(Fore.GREEN + f"Types in both files: {len(in_both)}")

    if only_in_file1:
        print(Fore.YELLOW + f"\nTypes only in {file1} ({len(only_in_file1)}):")
        for name in sorted(only_in_file1):
            print(f"\t{name}")

    if only_in_file2:
        print(Fore.YELLOW + f"\nTypes only in {file2} ({len(only_in_file2)}):")
        for name in sorted(only_in_file2):
            print(f"\t{name}")

    if not only_in_file1 and not only_in_file2:
        print(Fore.GREEN + "Files contain identical type sets.")


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
    compare_types(args.file1, args.file2)
