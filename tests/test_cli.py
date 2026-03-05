import subprocess
import sys


class TestCLI:
    def test_help_shows_subcommands(self):
        result = subprocess.run(
            [sys.executable, "-m", "dayz_admin_tools", "--help"],
            capture_output=True,
            text=True,
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
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--type" in result.stdout
        assert "--dir" in result.stdout

    def test_no_args_shows_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "dayz_admin_tools"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
