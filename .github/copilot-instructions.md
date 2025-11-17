<!-- Copilot instructions for working on the dayz-admin repo -->
# dayz-admin — AI coding assistant instructions

Purpose: Quickly orient an AI coding agent to be productive in this repository. Be specific and actionable — reference files, commands, and local conventions.

- **Quick setup**:
  - **Install dependencies**: project uses Poetry. Run `poetry install` to create the virtual environment and install packages listed in `pyproject.toml`.
  - **Run a script**: use the Poetry environment: `poetry run python standalone/validator.py -t JSON -d /path/to/profiles` (see `README.md` for example flags).
  - **Run GUI** (requires `PyQt6`): `poetry run python src/main.py` or `poetry run python src/validatorUI.py` for the validator UI.

- **Project layout (important files/directories)** — scan these first:
  - `dayz_admin_tools/` — main package. Key subfolders:
    - `utilities/files/` — `fManager.py` provides filesystem helpers: `find_files`, `backup`, `return_filename`.
    - `utilities/traders/` — conversion/market logic. Two flavours in repo: `expansion/` and `traderplus/` (see `Items.py`, `Item.py`, `Vendors.py`). These modules load JSON market files and validate them against local schemas.
    - `utilities/economy/` — types and schemas for XML/market processing (`Types.py`).
  - `standalone/` — CLI utilities (small programs with `argparse`). Examples: `validator.py`, `items_loader.py`, `types_loader.py`, `traderplus_to_expansion.py`.
  - `src/` — WIP GUI and configuration: `src/main.py`, `src/validatorUI.py`, and `src/config/`.
  - `tests/` — contains simple/unimplemented tests (`test_json.py`, `test_xml.py`). Tests currently are placeholders.

- **Key runtime/config notes**:
  - `ROOT_DIR` is defined in `dayz_admin_tools/config.py` and used by many utilities to locate schemas and resource files. Use `ROOT_DIR` when forming file paths inside the package.
  - GUI configuration is stored at `src/config/app-config.json` — created on first GUI run. Don't assume it exists in a CI environment.
  - JSON schemas are embedded near the modules that use them, e.g. `dayz_admin_tools/utilities/traders/expansion/schemas/items.schema.json`.

- **Common patterns found in code** (use these when changing code):
  - Schema-first validation: JSON documents are validated via `jsonschema.validate` before processing (see `Items.load_items`). If you add new JSON handling, follow the same validation pattern and return clear errors.
  - File discovery uses `FileManager.find_files(root, extension)` to recursively collect files. Prefer reusing it instead of reinventing os.walk logic.
  - JSON traversal uses `jsonpath_ng` with `jsonpath_ng.ext.parser` for locating nested values (e.g., `$.Items..ClassName`). Use the same library if adding complex JSON queries.
  - CLI utilities use `argparse` and present usage in README; follow the same `-d/--dir`, `-f/--file`, and `-t/--type` flag conventions when adding scripts.
  - Colorized terminal output uses `colorama` (`Fore`, `Back`) — maintain human-readable messages and consistent ANSI coloring.

- **Developer workflows & commands**:
  - Install deps and enter environment: `poetry install` then `poetry shell` or prefix commands with `poetry run`.
  - Run unit tests: `poetry run pytest` (tests are small/unimplemented; expect failures until tests are implemented).
  - Lint / format: `black` and `isort` are listed in `pyproject.toml` — run them inside the Poetry environment.

- **When editing/adding utilities**:
  - Add modules under `dayz_admin_tools/utilities/<category>/` and include an `__init__.py`.
  - If the utility is a CLI tool, add a corresponding small script under `standalone/` that uses `argparse` and imports your utility functions from the package. Keep CLI parsing and business logic separated.
  - If your code touches file resolution, prefer using `ROOT_DIR` + relative package paths (see `Items.__init__` which opens schema using `ROOT_DIR + '/dayz_admin_tools/...'`).

- **Integration points & expectations**:
  - Schemas (XSD/JSON) under `utilities/*/schemas/` are authoritative — changes to schemas affect multiple utilities.
  - Many tools assume DayZ Profile directory structure (types.xml, Markets folder). When writing tests or adding tooling, use fixture directories that mimic a small Profile layout.

- **Tests / CI notes**:
  - There is no CI config in the repository. Tests use `unittest`/pytest-compatible patterns but are placeholders — do not rely on existing test coverage.

If anything here is unclear or you'd like me to emphasize different areas (for example: GUI internals, a specific conversion script, or a suggested test harness), tell me which areas to expand and I'll iterate.
