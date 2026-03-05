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
