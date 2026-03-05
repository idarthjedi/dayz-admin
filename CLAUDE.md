# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DayZ Admin Tools — a collection of Python CLI utilities and a WIP GUI for managing DayZ game server configurations. Handles validation, conversion, and analysis of types.xml files, Expansion Market JSON files, and TraderPlus trader files.

## Setup & Commands

- **Package manager**: uv
- **Install**: `uv sync` (add `--group dev` for dev tools)
- **Run a standalone script**: `uv run python standalone/validator.py -t JSON -d /path/to/dir`
- **Run CLI**: `uv run dayz-admin <subcommand>` (unified entry point)
- **Run GUI**: `uv run python src/main.py` (requires PyQt6)
- **Run tests**: `uv run pytest`
- **Format**: `uv run black .` and `uv run isort .`
- **Python version**: 3.9+

## Architecture

### `dayz_admin_tools/` — Main Package
- `cli.py` — Unified CLI entry point (`dayz-admin <subcommand>`). Subcommands: `validate`, `types`, `items`, `airdrop`, `convert`, `compare`
- `config.py` — Defines `ROOT_DIR` (project root). Always use `ROOT_DIR` for path resolution within the package.
- `defaults.py` — Centralized constants (prices, thresholds, market file defaults)
- `log.py` — Logging setup with `ColoramaFormatter` for colored terminal output
- `utilities/text.py` — Shared text processing: `strip_codes`, `safe_filename`, `remove_comments`, `remove_notes`
- `utilities/files/` — File helpers: `fManager.py` (uses `pathlib`), `xml.py`, `json.py`
- `utilities/economy/` — `Types.py` / `Type.py` for DayZ types.xml processing
- `utilities/traders/expansion/` — Expansion Market item handling with JSON schema validation (`schemas/items.schema.json`)
- `utilities/traders/traderplus/` — TraderPlus item/vehicle parts parsing

### `standalone/` — CLI Tools (argparse-based)
Each script is a self-contained CLI tool that imports from `dayz_admin_tools`. Key tools: `validator.py`, `items_loader.py`, `types_loader.py`, `traderplus_to_expansion.py`, `types_to_market.py`, `compare_type_file.py`.

### `src/` — WIP GUI Application
PyQt6-based GUI (`src/main.py`, `src/validatorUI.py`). Config stored at `src/config/app-config.json` (auto-created on first run; don't assume it exists).

## Code Conventions

- **Schema-first validation**: JSON files are validated via `jsonschema.validate` before processing. Follow this pattern for new JSON handling.
- **File discovery**: Use `FileManager.find_files(root, extension)` — uses `pathlib.rglob` internally.
- **JSON path queries**: Use `jsonpath_ng` with `jsonpath_ng.ext.parser` for nested value extraction.
- **CLI flags**: Follow existing conventions: `-d/--dir`, `-f/--file`, `-t/--type`.
- **Logging**: Use `dayz_admin_tools.log.setup_logging()` for colored terminal output via `logging` module. Prefer `logging` over `print()`.
- **Text processing**: Use shared functions from `dayz_admin_tools.utilities.text` — don't duplicate `strip_codes`, `safe_filename`, etc.
- **Constants**: Use `dayz_admin_tools.defaults` for magic numbers (prices, thresholds). Don't hardcode.
- **Formatting**: `black` (v25.11.0) and `isort` (v6.1.0) — in dev dependency group.
- **New utilities**: Add modules under `dayz_admin_tools/utilities/<category>/` with `__init__.py`. Add a subcommand in `cli.py`. Keep CLI parsing separate from business logic.

## Key Dependencies

lxml, jsonschema, jsonpath-ng, colorama, PyQt6
