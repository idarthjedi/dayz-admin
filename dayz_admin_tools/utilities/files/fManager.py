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
