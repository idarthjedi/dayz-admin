# Simplify Review — 2026-03-26

Code review and cleanup of the codebase improvement commit (`dee6a14`). Three parallel reviews were run (reuse, quality, efficiency) and all actionable findings were fixed.

**14 files changed, 132 insertions, 163 deletions.**

## Code Reuse Fixes

### 1. Wire up `defaults.py` constants (all previously dead code)

| Constant | Wired to |
|----------|----------|
| `DEFAULT_PRICE` | `cli.py`, `traderplus_to_expansion.py`, `traderplusparts_to_vehicle_expansion.py` |
| `GENERIC_VEHICLE_PARTS` | `traderplusparts_to_vehicle_expansion.py` (removed local duplicate list) |
| `CONFIG_VERSION` | `src/config/config.py` |
| `MARKET_FILE_VERSION`, `MARKET_DEFAULT_ICON`, `MARKET_DEFAULT_COLOR`, `MARKET_DEFAULT_IS_EXCHANGE`, `MARKET_DEFAULT_INIT_STOCK_PERCENT` | `Items.file_header()` |
| `DEFAULT_SELL_PRICE_PERCENT`, `DEFAULT_MAX_STOCK_THRESHOLD`, `DEFAULT_MIN_STOCK_THRESHOLD`, `DEFAULT_QUANTITY_PERCENT` | `Item.create_new()` |

### 2. Extract duplicated airdrop section-mapping logic

The `match/case` block that maps aliases (`"d"`, `"med"`, `"b"`, `"mil"`) to airdrop container suffixes was duplicated verbatim in `cli.py` and `airdrop_loader.py`.

**Fix:** Added `AIRDROP_SECTION_MAP` dict and `AIRDROP_CONTAINER_BASE` string to `defaults.py`. Both call sites now do a single dict lookup:

```python
suffix = AIRDROP_SECTION_MAP.get(args.section.lower(), "")
section = AIRDROP_CONTAINER_BASE + suffix
```

## Code Quality Fixes

### 3. Replace `print(Fore.*)` with `logging` in `compare_type_file.py`

`compare_types()` used raw `print(Fore.RED + ...)` / `print(Fore.GREEN + ...)` calls. Replaced with `log.error()`, `log.info()`, `log.warning()` using the project's `ColoramaFormatter`, which provides color automatically. Added `setup_logging()` call in the `__main__` block.

### 4. Remove dead commented-out code

- `Items.py` (expansion): Removed 15-line block of commented-out XML processing code (lines 93-107)
- `airdrop_loader.py`: Removed 18 lines of commented-out example calls (lines 155-172)
- `Items.py` (traderplus): Removed `# _types = {}`
- `Vehicle_Parts.py`: Removed `# _types = {}` and `# new_lines.append(line.replace(...))`

### 5. Remove unnecessary comments

Removed "what" comments that restated the code:
- `# remove all the \t and \n from the start/end` before `strip_codes()` call (in both `Items.py` and `Vehicle_Parts.py`)

### 6. Clean up unused imports

- `traderplusparts_to_vehicle_expansion.py`: Removed `re`, `Back`, `Fore`, `Style`
- `traderplus_to_expansion.py`: Removed `re`, `Back`, `Fore`, `Style`

## Efficiency Fixes

### 7. Pre-compile regexes at module level in `text.py`

`remove_notes()` and `remove_comments()` called `re.compile()` on every invocation. These functions are called per-line in tight loops inside `clean_file()`. Moved regex compilation to module-level constants `_NOTES_RE` and `_COMMENTS_RE`.

### 8. Change `GENERIC_VEHICLE_PARTS` from `list` to `frozenset`

Used for `in` membership checks inside nested loops. `frozenset` provides O(1) lookups vs O(n) for lists.

### 9. Change `unique_parts_names` from `list` to `set`

In `traderplusparts_to_vehicle_expansion.py`, this was used for deduplication via `if x not in list` + `list.append(x)` — an O(n^2) pattern. Changed to `set` with `.add()` for O(n) total.

### 10. Remove redundant `float()` casts

`math.floor(float(price) * multiplier)` — `price` is already `int`, and `int * float` produces `float` in Python. Removed the unnecessary `float()` wrapper in all 6 occurrences across both converter scripts.

### 11. Move SAX parser creation outside the loop in `xml.py`

`XMLManager.validate_files()` was creating a new SAX parser and `ContentHandler` for every file. Since `ContentHandler()` is stateless, the parser can be created once and reused.

## Bug Fixes

### 12. `ColoramaFormatter.format()` mutates `LogRecord` in place

The original code set `record.msg = f"{color}{record.msg}{reset}"` directly on the record. If a second handler (e.g., a file handler) processes the same record, it receives color escape codes in the message. Fixed by creating a shallow copy via `logging.makeLogRecord(record.__dict__)`.

### 13. `setup_logging()` accumulates duplicate handlers

Each call to `setup_logging()` appended a new `StreamHandler` without clearing existing ones. Multiple calls (e.g., in tests) caused duplicate log lines. Fixed by adding `root.handlers.clear()` before adding the new handler.

### 14. `loadConfig()` — TOCTOU race and potential `UnboundLocalError`

The original code had:
1. A redundant `if os.path.exists()` check after just creating the file (TOCTOU pattern)
2. If the config file didn't exist AND the fallback copy failed, the variables `_profiles_directory` etc. would never be assigned, causing `UnboundLocalError` at the `return` statement

Fixed by removing the redundant existence check — after the copy-if-missing block, the file is opened directly and errors are raised cleanly.
