import argparse
import logging
import sys

from colorama import init as colorama_init

from dayz_admin_tools.log import setup_logging

log = logging.getLogger(__name__)


def cmd_validate(args: argparse.Namespace) -> None:
    from dayz_admin_tools.utilities.files.json import JSONManager
    from dayz_admin_tools.utilities.files.xml import XMLManager

    for directory in args.dir:
        if args.type in ("JSON", "BOTH"):
            resp, count, files = JSONManager.validate_files(directory)
            log.info(f"{count} JSON files validated in {directory}")
            if not resp:
                log.error("The following files failed JSON validation:")
                for err in files:
                    log.error(f"\t{err}")

        if args.type in ("XML", "BOTH"):
            resp, count, files = XMLManager.validate_files(directory)
            log.info(f"{count} XML files validated in {directory}")
            if not resp:
                log.error("The following files failed XML validation:")
                for err in files:
                    log.error(f"\t{err}")


def cmd_types(args: argparse.Namespace) -> None:
    from standalone.types_loader import load_profiles
    load_profiles(args.dir)


def cmd_items(args: argparse.Namespace) -> None:
    from standalone.items_loader import load_items
    load_items(args.dir, args.ignore_variants)


def cmd_airdrop(args: argparse.Namespace) -> None:
    from standalone.airdrop_loader import main as airdrop_main
    section = "ExpansionAirdropContainer"
    match args.section.lower():
        case "d" | "default":
            pass
        case "med" | "medical":
            section += "_Medical"
        case "b" | "basebuilding":
            section += "_Basebuilding"
        case "mil" | "military":
            section += "_Military"
    airdrop_main(args.dir, args.item, args.file, section)


def cmd_convert_traderplus(args: argparse.Namespace) -> None:
    from standalone.traderplus_to_expansion import main as convert_main
    kwargs = {"filename": args.file}
    if args.multiplier:
        kwargs["multiplier"] = args.multiplier
    convert_main(**kwargs)


def cmd_convert_vehicle_parts(args: argparse.Namespace) -> None:
    from standalone.traderplusparts_to_vehicle_expansion import main as convert_main
    kwargs = {"filename": args.file}
    if args.multiplier:
        kwargs["multiplier"] = args.multiplier
    convert_main(**kwargs)


def cmd_convert_types_to_market(args: argparse.Namespace) -> None:
    from standalone.types_to_market import convert_types
    convert_types(args.file, args.price, args.category)


def cmd_compare(args: argparse.Namespace) -> None:
    from standalone.compare_type_file import compare_types
    compare_types(args.file1, args.file2)


def main() -> None:
    colorama_init()

    parser = argparse.ArgumentParser(
        prog="dayz-admin",
        description="DayZ server administration tools",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet output (warnings and errors only)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate JSON and/or XML files")
    p_validate.add_argument("-t", "--type", choices=["JSON", "XML", "BOTH"], default="BOTH")
    p_validate.add_argument("-d", "--dir", action="append", required=True, help="Directory to validate")
    p_validate.set_defaults(func=cmd_validate)

    # types
    p_types = subparsers.add_parser("types", help="Load and validate types.xml files")
    p_types.add_argument("-d", "--dir", required=True, help="DayZ profiles directory")
    p_types.set_defaults(func=cmd_types)

    # items
    p_items = subparsers.add_parser("items", help="Load and validate market item files")
    p_items.add_argument("-d", "--dir", required=True, help="Expansion Market directory")
    p_items.add_argument("-iv", "--ignore_variants", action="store_true", default=False)
    p_items.set_defaults(func=cmd_items)

    # airdrop
    p_airdrop = subparsers.add_parser("airdrop", help="Update airdrop settings")
    p_airdrop.add_argument("-d", "--dir", required=True, help="Expansion config directory")
    p_airdrop.add_argument("-i", "--item", required=True, help="Item fragment to search for")
    p_airdrop.add_argument("-f", "--file", required=True, help="Market file to examine")
    p_airdrop.add_argument("-s", "--section", choices=["d", "default", "med", "medical", "b", "basebuilding", "mil", "military"], default="d")
    p_airdrop.set_defaults(func=cmd_airdrop)

    # convert subgroup
    p_convert = subparsers.add_parser("convert", help="Convert between trader formats")
    convert_sub = p_convert.add_subparsers(dest="convert_command")

    # convert traderplus
    p_tp = convert_sub.add_parser("traderplus", help="Convert TraderPlus to Expansion")
    p_tp.add_argument("-f", "--file", required=True, help="TraderPlus file to convert")
    p_tp.add_argument("-m", "--multiplier", type=float, help="Price multiplier")
    p_tp.set_defaults(func=cmd_convert_traderplus)

    # convert vehicle-parts
    p_vp = convert_sub.add_parser("vehicle-parts", help="Convert TraderPlus vehicle parts to Expansion")
    p_vp.add_argument("-f", "--file", required=True, help="TraderPlus vehicle parts file")
    p_vp.add_argument("-m", "--multiplier", type=float, help="Price multiplier")
    p_vp.set_defaults(func=cmd_convert_vehicle_parts)

    # convert types-to-market
    p_ttm = convert_sub.add_parser("types-to-market", help="Convert types.xml to market file")
    p_ttm.add_argument("-f", "--file", required=True, help="Types file to convert")
    p_ttm.add_argument("-p", "--price", type=int, default=500, help="Default price")
    p_ttm.add_argument("-c", "--category", required=True, help="Category name")
    p_ttm.set_defaults(func=cmd_convert_types_to_market)

    # compare
    p_compare = subparsers.add_parser("compare", help="Compare two types.xml files")
    p_compare.add_argument("-f1", "--file1", required=True, metavar="file1")
    p_compare.add_argument("-f2", "--file2", required=True, metavar="file2")
    p_compare.set_defaults(func=cmd_compare)

    args = parser.parse_args()
    setup_logging(verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False))

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.parse_args([args.command, "--help"])


if __name__ == "__main__":
    main()
