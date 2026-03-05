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
