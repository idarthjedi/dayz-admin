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
