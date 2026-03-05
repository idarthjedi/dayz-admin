# Codebase Improvement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix critical bugs, migrate to uv, modernize the codebase, consolidate CLI, add tests, and clean up the GUI.

**Architecture:** Six sequential phases. Each phase builds on the previous. Phase 1 fixes bugs in place. Phase 2 migrates packaging. Phases 3-4 restructure code. Phase 5 adds tests against the new APIs. Phase 6 cleans up the GUI layer.

**Tech Stack:** Python 3.9+, uv, pytest, pathlib, logging, dataclasses, argparse subparsers, lxml, jsonschema, jsonpath-ng, colorama, PyQt6

---

## Phase 1: Critical Bug Fixes

### Task 1.1: Fix config version logic and raise-string bug

**Files:**
- Modify: `src/config/config.py:28-39`

**Step 1: Fix the raise-string on line 39**

Replace:
```python
            except json.JSONDecodeError as error:
                raise "Cannot validate app-config.json"
```
With:
```python
            except json.JSONDecodeError as error:
                raise ValueError(f"Cannot validate app-config.json: {error}") from error
```

**Step 2: Fix the version check logic on lines 32-37**

The config saves version `1.1` (line 57) but checks `<= 1.0` (line 32). Since breaking changes are fine, simplify: always expect the latest format. Replace lines 28-37:
```python
                _config_version = float(config["config-version"])
                _profiles_directory = config["properties"]["dayz-profile-dir"]
                _json_directory = config["properties"]["other_dirs"]["json"]
                _xml_directory = config["properties"]["other_dirs"]["xml"]
                _market_directory = config["properties"].get("market-dir", "")
                _trader_directory = config["properties"].get("trader-dir", "")
```

**Step 3: Add file I/O error handling around config load**

Wrap the file open on line 25 with error handling. Replace lines 24-39:
```python
    if os.path.exists(f"{cur_dir}/app-config.json"):
        try:
            with open(f"{cur_dir}/app-config.json") as config_file:
                config = json.load(config_file)
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"Cannot load app-config.json: {error}") from error

        _profiles_directory = config["properties"]["dayz-profile-dir"]
        _json_directory = config["properties"]["other_dirs"]["json"]
        _xml_directory = config["properties"]["other_dirs"]["xml"]
        _market_directory = config["properties"].get("market-dir", "")
        _trader_directory = config["properties"].get("trader-dir", "")
```

**Step 4: Fix saveConfig type hints on line 52**

Replace:
```python
def saveConfig(
    profileDir: str, market_dir: str, traders_dir: str, json_items: [], xml_items: []
) -> bool:
```
With:
```python
def saveConfig(
    profileDir: str, market_dir: str, traders_dir: str, json_items: list, xml_items: list
) -> bool:
```

**Step 5: Commit**

```
git add src/config/config.py
git commit -m "fix: config version logic, raise-string bug, and type hints"
```

---

### Task 1.2: Fix type hints in expansion Item.py

**Files:**
- Modify: `dayz_admin_tools/utilities/traders/expansion/Item.py:1-49`

**Step 1: Fix type annotations**

`type[Item]` means "the Item class itself" -- these should be `Item | None` and `list[Item]`. The file already has `from __future__ import annotations` so forward references work. Replace the full file:

```python
from __future__ import annotations

from typing import Optional


class Item:

    _name: str
    _filesource: str
    _parent: Optional[Item]
    _variants: Optional[list[Item]]

    def __init__(
        self,
        name: str,
        filesource: str,
        parent: Optional[Item] = None,
        variants: Optional[list[Item]] = None,
    ):
        self._name = name
        self._filesource = filesource
        self._parent = parent
        self._variants = variants

    @property
    def name(self) -> str:
        return self._name

    @property
    def filesource(self) -> str:
        return self._filesource

    @property
    def parent(self) -> Optional[Item]:
        return self._parent

    @parent.setter
    def parent(self, parent: Optional[Item]) -> None:
        self._parent = parent

    @property
    def variants(self) -> Optional[list[Item]]:
        return self._variants

    @variants.setter
    def variants(self, variants: Optional[list[Item]]) -> None:
        self._variants = variants

    @staticmethod
    def create_new(classname: str) -> dict:
        return {
            "ClassName": classname,
            "MaxPriceThreshold": 0,
            "MinPriceThreshold": 0,
            "SellPricePercent": -1.0,
            "MaxStockThreshold": 1,
            "MinStockThreshold": 1,
            "QuantityPercent": -1,
            "SpawnAttachments": [],
            "Variants": [],
        }
```

**Step 2: Commit**

```
git add dayz_admin_tools/utilities/traders/expansion/Item.py
git commit -m "fix: correct type hints in expansion Item.py (type[Item] -> Optional[Item])"
```

---

### Task 1.3: Fix FileManager abstract class and super() calls

**Files:**
- Modify: `dayz_admin_tools/utilities/files/fManager.py`
- Modify: `dayz_admin_tools/utilities/files/xml.py:27`
- Modify: `dayz_admin_tools/utilities/files/json.py:25`

**Step 1: Fix FileManager -- remove broken abstract pattern**

The class has `@staticmethod` combined with `@abstractmethod` which does not enforce anything. Also, the `__init__` is abstract but the class is only used for its static methods. Replace the full file:

```python
import os
import shutil
from datetime import datetime


class FileManager:
    """Base file manager with shared static utilities."""

    @staticmethod
    def backup(fullpath_filename: str) -> None:
        uniqueness_name = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        file_parts = os.path.splitext(fullpath_filename)
        new_filename = f"{file_parts[0]}-BACKUP.{uniqueness_name}.{file_parts[1]}"
        shutil.copy(fullpath_filename, new_filename)

    @staticmethod
    def return_filename(fullpath_filename: str, split_extension: bool = False) -> tuple:
        if not split_extension:
            return os.path.basename(fullpath_filename)
        else:
            return os.path.splitext(fullpath_filename)

    @staticmethod
    def return_dirname(fullpath_filename: str) -> str:
        return os.path.dirname(fullpath_filename)

    @staticmethod
    def find_files(filepath: str, extension: str) -> list:
        file_names = []
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(extension) and not file.startswith("."):
                    file_names.append(os.path.join(root, file))
        return file_names
```

**Step 2: Fix XMLManager super() call and remove unnecessary init**

Replace `dayz_admin_tools/utilities/files/xml.py` entirely:

```python
import xml.sax
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from dayz_admin_tools.utilities.files.fManager import FileManager


class XMLManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        validated = True
        output = []
        file_count = 0

        files = FileManager.find_files(filepath, ".xml")

        for file in files:
            try:
                parser = make_parser()
                parser.setContentHandler(ContentHandler())
                parser.parse(file)
                file_count += 1
            except xml.sax.SAXParseException:
                output.append(file)
                validated = False

        return validated, file_count, output
```

**Step 3: Fix JSONManager super() call and remove unnecessary init**

Replace `dayz_admin_tools/utilities/files/json.py` entirely:

```python
import json

from dayz_admin_tools.utilities.files.fManager import FileManager


class JSONManager(FileManager):

    @staticmethod
    def validate_files(filepath: str) -> tuple[bool, int, list]:
        validated = True
        output = []
        file_count = 0

        files = FileManager.find_files(filepath, ".json")
        for file in files:
            with open(file) as validate_file:
                try:
                    json.load(validate_file)
                    file_count += 1
                except json.JSONDecodeError:
                    output.append(file)
                    validated = False

        return validated, file_count, output
```

**Step 4: Commit**

```
git add dayz_admin_tools/utilities/files/fManager.py dayz_admin_tools/utilities/files/xml.py dayz_admin_tools/utilities/files/json.py
git commit -m "fix: remove broken abstract pattern from FileManager, fix super() calls"
```

---

### Task 1.4: Fix incomplete/dead code

**Files:**
- Modify: `standalone/compare_type_file.py`
- Delete: `dayz_admin_tools/utilities/traders/traderplus/Item.py`
- Delete: `dayz_admin_tools/utilities/traders/expansion/Vendors.py`

**Step 1: Implement compare_type_file.py**

Lines 45-46 are commented out. The script parses two type files but does nothing. Implement the comparison:

```python
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
        "-f1", "--file1",
        help="Specify the first types file to compare.",
        action="store", required=True, metavar="file1",
    )
    parser.add_argument(
        "-f2", "--file2",
        help="Specify the second types file to compare.",
        action="store", required=True, metavar="file2",
    )

    if len(sys.argv) < 3:
        parser.print_help()
        exit()

    args = parser.parse_args()
    compare_types(args.file1, args.file2)
```

**Step 2: Delete empty files**

Remove `dayz_admin_tools/utilities/traders/traderplus/Item.py` (empty) and `dayz_admin_tools/utilities/traders/expansion/Vendors.py` (empty).

**Step 3: Commit**

```
git add standalone/compare_type_file.py
git rm dayz_admin_tools/utilities/traders/traderplus/Item.py dayz_admin_tools/utilities/traders/expansion/Vendors.py
git commit -m "fix: implement compare_type_file.py, remove empty dead files"
```

---

### Task 1.5: Fix airdrop_loader.py bugs

**Files:**
- Modify: `standalone/airdrop_loader.py:121,133-143`

**Step 1: Fix the typo on line 137 and duplicate match cases**

Line 137 has `section = +"_Medical"` (unary plus on string -- will crash). Lines 136 and 140 both match `"m"` (duplicate case). Replace lines 133-143:

```python
    match args.section.lower():
        case "d" | "default":
            pass
        case "med" | "medical":
            section += "_Medical"
        case "b" | "basebuilding":
            section += "_Basebuilding"
        case "mil" | "military":
            section += "_Military"
        case _:
            pass
```

Also update the `choices` on line 121 to match:
```python
        choices=["d", "default", "med", "medical", "b", "basebuilding", "mil", "military"],
```

**Step 2: Commit**

```
git add standalone/airdrop_loader.py
git commit -m "fix: airdrop_loader section match bugs (typo, duplicate cases)"
```

---

## Phase 2: uv Migration

### Task 2.1: Convert pyproject.toml from Poetry to PEP 621

**Files:**
- Modify: `pyproject.toml`

**Step 1: Rewrite pyproject.toml**

Replace the entire file:
```toml
[project]
name = "dayz-admin-tools"
version = "0.1.0"
description = "A collection of utilities for DayZ server administration"
authors = [{name = "idarthjedi", email = "jediah@logiodice.com"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "colorama>=0.4.6",
    "lxml>=5.3.0",
    "pyqt6>=6.4.2",
    "jsonschema>=4.17.3",
    "jsonpath-ng>=1.5.3",
]

[dependency-groups]
dev = [
    "black==25.11.0",
    "isort==6.1.0",
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.scripts]
dayz-admin = "dayz_admin_tools.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Note: `argparse` removed (stdlib). `black`/`isort` moved to dev. `pytest`/`pytest-cov` added to dev. Build backend changed from poetry-core to hatchling (uv-compatible). Entry point added for Phase 4.

**Step 2: Remove poetry.lock**

Delete `poetry.lock` if it exists.

**Step 3: Generate uv.lock and verify install**

Run: `uv sync`
Expected: Dependencies install successfully, `uv.lock` is created.

**Step 4: Verify the project works**

Run: `uv run python standalone/validator.py --help`
Expected: Help text prints without import errors.

**Step 5: Commit**

```
git add pyproject.toml uv.lock
git rm -f poetry.lock 2>/dev/null; true
git commit -m "build: migrate from Poetry to uv with PEP 621 pyproject.toml"
```

---

### Task 2.2: Update CLAUDE.md with new commands

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update the Setup and Commands section**

Replace references to Poetry with uv equivalents:
- `uv sync` replaces `poetry install`
- `uv run` replaces `poetry run`
- Add note about `uv sync --group dev` for dev tools
- Add `uv run dayz-admin <subcommand>` for the new CLI

**Step 2: Commit**

```
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for uv migration"
```

---

## Phase 3: Shared Utilities and Modernization

### Task 3.1: Extract duplicated text processing functions

**Files:**
- Create: `dayz_admin_tools/utilities/text.py`
- Modify: `dayz_admin_tools/utilities/traders/traderplus/Items.py`
- Modify: `dayz_admin_tools/utilities/traders/traderplus/Vehicle_Parts.py`
- Modify: `standalone/traderplus_to_expansion.py`
- Modify: `standalone/traderplusparts_to_vehicle_expansion.py`

**Step 1: Create shared text module**

Create `dayz_admin_tools/utilities/text.py`:
```python
import re


def strip_codes(source: str) -> str:
    """Strip control characters (newline, tab) and whitespace from a string."""
    control_chars = ["\n", "\t"]
    for c in control_chars:
        source = source.strip(c)
    return source.strip()


def safe_filename(source: str) -> str:
    """Replace invalid filename characters with underscores."""
    invalid = r'<>:"/\|?* ,'
    for char in invalid:
        source = source.replace(char, "_")
    return source


def remove_notes(string: str) -> str:
    """Remove <<note>> markers from a string."""
    pattern = r"(<<.*>>)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(1) is not None:
            return ""

    return regex.sub(_replacer, string)


def remove_comments(string: str) -> str:
    """Remove // and /* */ comments while preserving quoted strings."""
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)

    return regex.sub(_replacer, string)
```

**Step 2: Update traderplus/Items.py to use shared module**

Remove methods `_strip_codes`, `_safe_filename`, `_remove_notes`, `_remove_comments` (lines 61-107). Add import:
```python
from dayz_admin_tools.utilities.text import remove_comments, remove_notes, strip_codes
```
Replace `self._strip_codes(` with `strip_codes(`, `self._remove_comments(` with `remove_comments(`, `self._remove_notes(` with `remove_notes(`.

**Step 3: Update traderplus/Vehicle_Parts.py similarly**

Remove methods `_strip_codes`, `_safe_filename`, `_remove_notes`, `_remove_comments` (lines 67-113). Same import and call replacements.

**Step 4: Update standalone scripts**

In `standalone/traderplus_to_expansion.py`, remove `_strip_codes` and `_safe_filename` functions (lines 100-115). Add import:
```python
from dayz_admin_tools.utilities.text import strip_codes, safe_filename
```
Replace `_strip_codes(` with `strip_codes(` and `_safe_filename(` with `safe_filename(`.

In `standalone/traderplusparts_to_vehicle_expansion.py`, same changes (lines 117-132).

**Step 5: Commit**

```
git add dayz_admin_tools/utilities/text.py dayz_admin_tools/utilities/traders/traderplus/Items.py dayz_admin_tools/utilities/traders/traderplus/Vehicle_Parts.py standalone/traderplus_to_expansion.py standalone/traderplusparts_to_vehicle_expansion.py
git commit -m "refactor: extract duplicated text processing into shared module"
```

---

### Task 3.2: Create defaults/constants module

**Files:**
- Create: `dayz_admin_tools/defaults.py`

**Step 1: Create the defaults module**

```python
"""Central location for default values and constants used across the codebase."""

# Expansion Market file defaults
MARKET_FILE_VERSION = 12
MARKET_DEFAULT_COLOR = "FBFCFEFF"
MARKET_DEFAULT_ICON = "Deliver"
MARKET_DEFAULT_INIT_STOCK_PERCENT = 25.0
MARKET_DEFAULT_IS_EXCHANGE = 0

# Item defaults
DEFAULT_PRICE = 500
DEFAULT_SELL_PRICE_PERCENT = -1.0
DEFAULT_MAX_STOCK_THRESHOLD = 1
DEFAULT_MIN_STOCK_THRESHOLD = 1
DEFAULT_QUANTITY_PERCENT = -1

# Generic vehicle parts (common across all vehicle conversions)
GENERIC_VEHICLE_PARTS = [
    "SparkPlug",
    "CarBattery",
    "CarRadiator",
    "HeadlightH7",
    "TruckBattery",
]

# Config
CONFIG_VERSION = 1.1
```

**Step 2: Commit**

```
git add dayz_admin_tools/defaults.py
git commit -m "refactor: extract hardcoded values into defaults module"
```

Note: Updating all references to use these constants is done incrementally as files are touched in subsequent tasks.

---

### Task 3.3: Add logging framework

**Files:**
- Create: `dayz_admin_tools/log.py`

**Step 1: Create logging setup with colorama formatter**

```python
import logging
import sys

from colorama import Fore, Style


class ColoramaFormatter(logging.Formatter):
    """Logging formatter that uses colorama for colored terminal output."""

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        record.msg = f"{color}{record.msg}{reset}"
        return super().format(record)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure root logger with colorama-colored console output."""
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoramaFormatter("%(message)s"))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
```

**Step 2: Commit**

```
git add dayz_admin_tools/log.py
git commit -m "feat: add logging framework with colorama formatter"
```

Note: Migration of individual files from print() to logging happens incrementally in Phase 4 when the CLI is consolidated.

---

### Task 3.4: Migrate FileManager to pathlib

**Files:**
- Modify: `dayz_admin_tools/utilities/files/fManager.py`

**Step 1: Rewrite using pathlib**

```python
import shutil
from datetime import datetime
from pathlib import Path


class FileManager:
    """Base file manager with shared static utilities."""

    @staticmethod
    def backup(fullpath_filename: str) -> None:
        path = Path(fullpath_filename)
        uniqueness_name = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        new_filename = path.with_name(
            f"{path.stem}-BACKUP.{uniqueness_name}{path.suffix}"
        )
        shutil.copy(path, new_filename)

    @staticmethod
    def return_filename(fullpath_filename: str, split_extension: bool = False) -> tuple | str:
        path = Path(fullpath_filename)
        if not split_extension:
            return path.name
        else:
            return (str(path.with_suffix("")), path.suffix)

    @staticmethod
    def return_dirname(fullpath_filename: str) -> str:
        return str(Path(fullpath_filename).parent)

    @staticmethod
    def find_files(filepath: str, extension: str) -> list[str]:
        root = Path(filepath)
        return [
            str(p) for p in root.rglob(f"*{extension}")
            if not p.name.startswith(".")
        ]
```

**Step 2: Verify no regressions**

Run: `uv run python -c "from dayz_admin_tools.utilities.files.fManager import FileManager; print('OK')"`
Expected: prints `OK`

**Step 3: Commit**

```
git add dayz_admin_tools/utilities/files/fManager.py
git commit -m "refactor: migrate FileManager to pathlib"
```

---

## Phase 4: CLI Consolidation

### Task 4.1: Create unified CLI entry point

**Files:**
- Create: `dayz_admin_tools/cli.py`
- Create: `dayz_admin_tools/__main__.py`

**Step 1: Create the CLI module with subcommands**

```python
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
```

**Step 2: Create __main__.py for `python -m` support**

Create `dayz_admin_tools/__main__.py`:
```python
from dayz_admin_tools.cli import main

main()
```

**Step 3: Verify**

Run: `uv run dayz-admin --help`
Expected: Shows all subcommands.

Run: `uv run dayz-admin validate --help`
Expected: Shows validate-specific flags.

**Step 4: Commit**

```
git add dayz_admin_tools/cli.py dayz_admin_tools/__main__.py
git commit -m "feat: unified CLI entry point with subcommands"
```

---

## Phase 5: Tests

### Task 5.1: Create test infrastructure

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/fixtures/valid.xml`
- Create: `tests/fixtures/invalid.xml`
- Create: `tests/fixtures/valid.json`
- Create: `tests/fixtures/invalid.json`
- Delete: `tests/test_xml.py` (empty placeholder)
- Delete: `tests/test_json.py` (empty placeholder)

**Step 1: Create test fixtures**

`tests/fixtures/valid.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<types>
    <type name="TestItem">
        <nominal>10</nominal>
        <lifetime>3600</lifetime>
        <restock>0</restock>
        <min>5</min>
        <quantmin>-1</quantmin>
        <quantmax>-1</quantmax>
        <cost>100</cost>
        <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    </type>
</types>
```

`tests/fixtures/invalid.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<types>
    <type name="BrokenItem">
    <!-- missing closing tag -->
</types>
```

`tests/fixtures/valid.json`:
```json
{
    "m_Version": 12,
    "DisplayName": "Test Market",
    "Icon": "Deliver",
    "Color": "FBFCFEFF",
    "IsExchange": 0,
    "InitStockPercent": 25.0,
    "Items": [
        {
            "ClassName": "TestItem",
            "MaxPriceThreshold": 100,
            "MinPriceThreshold": 50,
            "SellPricePercent": -1.0,
            "MaxStockThreshold": 1,
            "MinStockThreshold": 1,
            "QuantityPercent": -1,
            "SpawnAttachments": [],
            "Variants": ["TestItem_Red", "TestItem_Blue"]
        }
    ]
}
```

`tests/fixtures/invalid.json`:
```
{"m_Version": 12, "Items": [{"ClassName": "Missing trailing bracket"]
```

**Step 2: Create conftest.py**

```python
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def valid_xml(fixtures_dir: Path) -> Path:
    return fixtures_dir / "valid.xml"


@pytest.fixture
def invalid_xml(fixtures_dir: Path) -> Path:
    return fixtures_dir / "invalid.xml"


@pytest.fixture
def valid_json(fixtures_dir: Path) -> Path:
    return fixtures_dir / "valid.json"


@pytest.fixture
def invalid_json(fixtures_dir: Path) -> Path:
    return fixtures_dir / "invalid.json"


@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path:
    return tmp_path
```

**Step 3: Remove placeholder tests**

Delete `tests/test_xml.py` and `tests/test_json.py`.

**Step 4: Commit**

```
git add tests/conftest.py tests/fixtures/
git rm tests/test_xml.py tests/test_json.py
git commit -m "test: add test infrastructure and fixtures"
```

---

### Task 5.2: Write tests for text processing utilities

**Files:**
- Create: `tests/test_text.py`

**Step 1: Write the tests**

```python
from dayz_admin_tools.utilities.text import (
    remove_comments,
    remove_notes,
    safe_filename,
    strip_codes,
)


class TestStripCodes:
    def test_strips_newlines(self):
        assert strip_codes("\nhello\n") == "hello"

    def test_strips_tabs(self):
        assert strip_codes("\thello\t") == "hello"

    def test_strips_mixed(self):
        assert strip_codes("\n\t  hello  \t\n") == "hello"

    def test_empty_string(self):
        assert strip_codes("") == ""

    def test_preserves_internal_spaces(self):
        assert strip_codes("hello world") == "hello world"


class TestSafeFilename:
    def test_replaces_spaces(self):
        assert safe_filename("hello world") == "hello_world"

    def test_replaces_special_chars(self):
        assert safe_filename('file<>:"/\\|?*name') == "file_________name"

    def test_replaces_commas(self):
        assert safe_filename("a,b,c") == "a_b_c"

    def test_clean_string_unchanged(self):
        assert safe_filename("clean_name") == "clean_name"


class TestRemoveNotes:
    def test_removes_notes(self):
        assert remove_notes("hello <<note>> world") == "hello  world"

    def test_no_notes(self):
        assert remove_notes("hello world") == "hello world"

    def test_multiple_notes(self):
        assert remove_notes("<<a>> text <<b>>") == " text "


class TestRemoveComments:
    def test_removes_single_line_comment(self):
        result = remove_comments("code // comment")
        assert result.strip() == "code"

    def test_preserves_quoted_strings(self):
        result = remove_comments('"hello // world"')
        assert result == '"hello // world"'

    def test_removes_multiline_comment(self):
        result = remove_comments("code /* comment */ more")
        assert result == "code  more"

    def test_no_comments(self):
        assert remove_comments("just code") == "just code"
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_text.py -v`
Expected: All tests PASS

**Step 3: Commit**

```
git add tests/test_text.py
git commit -m "test: add tests for text processing utilities"
```

---

### Task 5.3: Write tests for FileManager

**Files:**
- Create: `tests/test_file_manager.py`

**Step 1: Write the tests**

```python
from pathlib import Path

from dayz_admin_tools.utilities.files.fManager import FileManager


class TestFindFiles:
    def test_finds_json_files(self, tmp_dir: Path):
        (tmp_dir / "a.json").write_text("{}")
        (tmp_dir / "b.json").write_text("{}")
        (tmp_dir / "c.txt").write_text("not json")
        result = FileManager.find_files(str(tmp_dir), ".json")
        assert len(result) == 2
        assert all(f.endswith(".json") for f in result)

    def test_finds_nested_files(self, tmp_dir: Path):
        sub = tmp_dir / "subdir"
        sub.mkdir()
        (sub / "nested.xml").write_text("<root/>")
        result = FileManager.find_files(str(tmp_dir), ".xml")
        assert len(result) == 1

    def test_ignores_hidden_files(self, tmp_dir: Path):
        (tmp_dir / ".hidden.json").write_text("{}")
        (tmp_dir / "visible.json").write_text("{}")
        result = FileManager.find_files(str(tmp_dir), ".json")
        assert len(result) == 1

    def test_empty_directory(self, tmp_dir: Path):
        result = FileManager.find_files(str(tmp_dir), ".json")
        assert result == []


class TestReturnFilename:
    def test_returns_basename(self):
        result = FileManager.return_filename("/path/to/file.json")
        assert result == "file.json"

    def test_returns_split_extension(self):
        result = FileManager.return_filename("/path/to/file.json", split_extension=True)
        assert result[1] == ".json"


class TestReturnDirname:
    def test_returns_directory(self):
        result = FileManager.return_dirname("/path/to/file.json")
        assert result == "/path/to"


class TestBackup:
    def test_creates_backup(self, tmp_dir: Path):
        original = tmp_dir / "test.json"
        original.write_text('{"key": "value"}')
        FileManager.backup(str(original))
        backups = list(tmp_dir.glob("test-BACKUP.*"))
        assert len(backups) == 1
        assert backups[0].read_text() == '{"key": "value"}'
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_file_manager.py -v`
Expected: All tests PASS

**Step 3: Commit**

```
git add tests/test_file_manager.py
git commit -m "test: add tests for FileManager"
```

---

### Task 5.4: Write tests for XML and JSON validation

**Files:**
- Create: `tests/test_validators.py`

**Step 1: Write the tests**

```python
import json
from pathlib import Path

from dayz_admin_tools.utilities.files.json import JSONManager
from dayz_admin_tools.utilities.files.xml import XMLManager


class TestXMLValidator:
    def test_validates_well_formed_xml(self, tmp_dir: Path):
        xml_file = tmp_dir / "good.xml"
        xml_file.write_text('<?xml version="1.0"?><root><item/></root>')
        validated, count, errors = XMLManager.validate_files(str(tmp_dir))
        assert validated is True
        assert count == 1
        assert errors == []

    def test_detects_malformed_xml(self, tmp_dir: Path):
        xml_file = tmp_dir / "bad.xml"
        xml_file.write_text('<?xml version="1.0"?><root><unclosed>')
        validated, count, errors = XMLManager.validate_files(str(tmp_dir))
        assert validated is False
        assert len(errors) == 1

    def test_mixed_valid_and_invalid(self, tmp_dir: Path):
        (tmp_dir / "good.xml").write_text('<?xml version="1.0"?><root/>')
        (tmp_dir / "bad.xml").write_text("<root><broken>")
        validated, count, errors = XMLManager.validate_files(str(tmp_dir))
        assert validated is False
        assert count == 1
        assert len(errors) == 1

    def test_empty_directory(self, tmp_dir: Path):
        validated, count, errors = XMLManager.validate_files(str(tmp_dir))
        assert validated is True
        assert count == 0


class TestJSONValidator:
    def test_validates_well_formed_json(self, tmp_dir: Path):
        json_file = tmp_dir / "good.json"
        json_file.write_text(json.dumps({"key": "value"}))
        validated, count, errors = JSONManager.validate_files(str(tmp_dir))
        assert validated is True
        assert count == 1
        assert errors == []

    def test_detects_malformed_json(self, tmp_dir: Path):
        json_file = tmp_dir / "bad.json"
        json_file.write_text('{"key": missing_quotes}')
        validated, count, errors = JSONManager.validate_files(str(tmp_dir))
        assert validated is False
        assert len(errors) == 1

    def test_empty_directory(self, tmp_dir: Path):
        validated, count, errors = JSONManager.validate_files(str(tmp_dir))
        assert validated is True
        assert count == 0
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_validators.py -v`
Expected: All tests PASS

**Step 3: Commit**

```
git add tests/test_validators.py
git commit -m "test: add tests for XML and JSON validators"
```

---

### Task 5.5: Write tests for CLI entry point

**Files:**
- Create: `tests/test_cli.py`

**Step 1: Write the tests**

```python
import subprocess
import sys


class TestCLI:
    def test_help_shows_subcommands(self):
        result = subprocess.run(
            [sys.executable, "-m", "dayz_admin_tools", "--help"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "validate" in result.stdout
        assert "types" in result.stdout
        assert "items" in result.stdout
        assert "convert" in result.stdout
        assert "compare" in result.stdout

    def test_validate_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "dayz_admin_tools", "validate", "--help"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "--type" in result.stdout
        assert "--dir" in result.stdout

    def test_no_args_shows_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "dayz_admin_tools"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_cli.py -v`
Expected: All tests PASS

**Step 3: Commit**

```
git add tests/test_cli.py
git commit -m "test: add CLI integration tests"
```

---

## Phase 6: GUI Cleanup

### Task 6.1: Remove global state from validatorUI.py

**Files:**
- Modify: `src/validatorUI.py`

**Step 1: Replace globals with a dataclass and function parameters**

```python
import sys
from dataclasses import dataclass, field

from colorama import Fore
from colorama import init as colorama_init
from PyQt6.QtWidgets import QApplication, QMainWindow

from dayz_admin_tools.utilities.economy.Types import Types
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
```

**Step 2: Commit**

```
git add src/validatorUI.py
git commit -m "refactor: replace global state in validatorUI with dataclass"
```

---

### Task 6.2: Final cleanup and formatting

**Files:**
- Modify: `CLAUDE.md` (final updates)

**Step 1: Update CLAUDE.md architecture section**

Add entries for new modules:
- `dayz_admin_tools/cli.py` -- unified CLI entry point (`dayz-admin <subcommand>`)
- `dayz_admin_tools/log.py` -- logging setup with colorama formatter
- `dayz_admin_tools/defaults.py` -- centralized constants and default values
- `dayz_admin_tools/utilities/text.py` -- shared text processing (strip_codes, safe_filename, remove_comments, remove_notes)

Update test section: `uv run pytest` now runs real tests.

**Step 2: Run full test suite**

Run: `uv run pytest -v`
Expected: All tests PASS

**Step 3: Run formatters**

Run: `uv run black .` and `uv run isort .`

**Step 4: Commit any formatting changes**

```
git add -A
git commit -m "docs: final CLAUDE.md update and formatting pass"
```

---

## Summary of All Tasks

| Phase | Task | Description |
|-------|------|-------------|
| 1 | 1.1 | Fix config version logic, raise-string bug, and type hints |
| 1 | 1.2 | Fix expansion Item.py type hints |
| 1 | 1.3 | Fix FileManager abstract class and super() calls |
| 1 | 1.4 | Implement compare_type_file.py, delete dead files |
| 1 | 1.5 | Fix airdrop_loader.py section match bugs |
| 2 | 2.1 | Convert pyproject.toml to PEP 621 for uv |
| 2 | 2.2 | Update CLAUDE.md for uv |
| 3 | 3.1 | Extract duplicated text processing into shared module |
| 3 | 3.2 | Create defaults/constants module |
| 3 | 3.3 | Add logging framework |
| 3 | 3.4 | Migrate FileManager to pathlib |
| 4 | 4.1 | Create unified CLI entry point with subcommands |
| 5 | 5.1 | Create test infrastructure and fixtures |
| 5 | 5.2 | Tests for text processing |
| 5 | 5.3 | Tests for FileManager |
| 5 | 5.4 | Tests for XML and JSON validators |
| 5 | 5.5 | Tests for CLI |
| 6 | 6.1 | Remove global state from validatorUI |
| 6 | 6.2 | Final cleanup and formatting |
