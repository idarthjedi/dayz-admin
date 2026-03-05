# Codebase Improvement Design

Date: 2026-03-04
Status: Approved

## Overview

Comprehensive improvement plan for the dayz-admin-tools codebase. Breaking changes are acceptable. Major restructuring including uv migration, CLI consolidation, and modernization of core patterns.

## Current State

The codebase has good domain knowledge but needs architectural hardening:
- Critical bugs in config handling (version logic, raise-string)
- Code duplication across 4 files (text processing helpers)
- Empty/incomplete modules (TraderPlus Item.py, compare_type_file.py)
- No real tests (placeholders only)
- Global state in GUI code
- Mixed generated/hand-written UI files
- Poetry for packaging (migrating to uv)
- print() + colorama for output (no structured logging)
- os.path throughout (migrating to pathlib)

## Phase 1: Critical Bug Fixes

### Config version logic (`src/config/config.py`)
- Fix version check: saves `1.1` but checks `<= 1.0`, causing logic mismatch
- Replace `raise "Cannot validate..."` with `raise ValueError(...)`
- Add file I/O error handling around config load/save

### Incorrect type hints (`dayz_admin_tools/utilities/traders/expansion/Item.py`)
- Change `type[Item]` to `Optional[Item]` for parent/variant references

### Broken abstract class (`dayz_admin_tools/utilities/files/fManager.py`)
- Fix `FileManager` — static methods marked abstract don't work as intended
- Fix `super(XMLManager, XMLManager).find_files()` calls to `FileManager.find_files()`

### Incomplete/dead code
- Fix or remove `standalone/compare_type_file.py` (currently a no-op, lines 45-46 commented out)
- Remove empty `dayz_admin_tools/utilities/traders/traderplus/Item.py` or implement it

## Phase 2: uv Migration + pyproject.toml Modernization

### Poetry to uv
- Convert `[tool.poetry.dependencies]` to PEP 621 `[project.dependencies]`
- Convert `[tool.poetry]` metadata to `[project]` section
- Remove `poetry.lock`, generate `uv.lock`
- Add `requires-python = ">=3.9"`

### Dependency reorganization
- Move `black`, `isort` to `[dependency-groups]` dev group
- Add `pytest`, `pytest-cov` to dev group
- Remove `argparse` from dependencies (it's stdlib)

### Entry point
- Add `[project.scripts] dayz-admin = "dayz_admin_tools.cli:main"` (for Phase 4)

### Developer workflow update
- `uv sync` replaces `poetry install`
- `uv run` replaces `poetry run`
- Update CLAUDE.md

## Phase 3: Shared Utilities + Modernization

### Extract duplicated code
- Create `dayz_admin_tools/utilities/text.py` with:
  - `strip_codes()` (from 4 files)
  - `safe_filename()` (from 4 files)
  - `remove_comments()` (from 2 files)
  - `remove_notes()` (from 2 files)
- Remove duplicates from: `standalone/traderplus_to_expansion.py`, `standalone/traderplusparts_to_vehicle_expansion.py`, `traderplus/Items.py`, `traderplus/Vehicle_Parts.py`

### Modernize core patterns
- `os.path` -> `pathlib.Path` throughout
- `print()` + `colorama` -> `logging` module with custom colorama formatter
- Magic string keys -> constants in `dayz_admin_tools/defaults.py`
- Manual `__init__` data containers -> `dataclasses` (Expansion `Item` is primary candidate)
- Add type hints to all public functions and methods

### Refactor class design
- Both `Items` classes: replace `dict` inheritance with composition
- `FileManager`: concrete utility class with static methods (drop broken abstract pattern)
- TraderPlus `Item.py`: implement to match Expansion `Item.py` pattern, or remove

### Extract hardcoded values
- Create `dayz_admin_tools/defaults.py` for prices, stock thresholds, schema versions, section mappings

## Phase 4: CLI Consolidation

### Unified entry point
- Create `dayz_admin_tools/cli.py` using argparse subparsers
- Subcommands:
  - `dayz-admin validate` (validator.py)
  - `dayz-admin types` (types_loader.py)
  - `dayz-admin items` (items_loader.py)
  - `dayz-admin airdrop` (airdrop_loader.py)
  - `dayz-admin convert traderplus` (traderplus_to_expansion.py)
  - `dayz-admin convert vehicle-parts` (traderplusparts_to_vehicle_expansion.py)
  - `dayz-admin convert types-to-market` (types_to_market.py)
  - `dayz-admin compare` (compare_type_file.py)

### Refactor standalone scripts
- Extract business logic from `if __name__ == "__main__"` into importable functions
- Keep standalone scripts as thin wrappers during transition
- Add input validation: verify directories exist, files readable, numeric args valid

### Shared CLI flags
- `--verbose` / `--quiet` mapped to log levels
- `--debug` replaces scattered `_DEBUG` global
- Consistent error output format

## Phase 5: Tests

### Infrastructure
- `pytest` + `pytest-cov` in dev dependencies
- `tests/fixtures/` with minimal sample data: types.xml, market JSON, TraderPlus config, airdrop settings JSON
- `tests/conftest.py` with shared fixtures (temp dirs, sample files)

### Unit tests (priority order)
1. `test_file_manager.py` — find_files(), backup(), return_filename()
2. `test_xml_manager.py` — well-formed and malformed XML validation
3. `test_json_manager.py` — well-formed and malformed JSON validation
4. `test_types.py` — Types.load_types() schema validation, duplicate detection
5. `test_items.py` — Items.load_items() schema validation, duplicate detection, variants
6. `test_text.py` — strip_codes, safe_filename, remove_comments, remove_notes
7. `test_config.py` — config load/save round-trip, version handling, missing file

### CLI integration tests
- `test_cli.py` — invoke each subcommand with fixtures, verify exit codes and output
- Error cases: missing dirs, malformed files, invalid args

### Out of scope
- GUI tests (WIP, not worth investment yet)

## Phase 6: GUI Cleanup

### Remove global state (`validatorUI.py`)
- Replace 5 mutable globals with a config dataclass
- Create QApplication once at app level, not inside readconfig()

### Separate generated and custom UI code
- Generated UI -> `mainUI_generated.py`, `mainConfig_generated.py`
- Custom logic in subclasses: `mainUI.py`, `mainConfig.py`

### Decouple business logic from UI
- Move Types(), Items(), JSONManager instantiation out of setupUi()
- Config loading in application startup, not UI setup

### Fix initialization
- `self._loaded = None` -> `self._loaded = False`
- Validate instance variables before use

## Dependencies Between Phases

- Phase 1 is independent, do first
- Phase 2 is independent of Phase 1, but do after for clean git history
- Phase 3 depends on Phase 2 (new pyproject.toml structure)
- Phase 4 depends on Phase 3 (shared utilities, modernized patterns)
- Phase 5 depends on Phase 3 and 4 (tests need stable APIs)
- Phase 6 depends on Phase 3 (logging, pathlib, dataclasses)
