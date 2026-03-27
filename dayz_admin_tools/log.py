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
        record = logging.makeLogRecord(record.__dict__)
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

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoramaFormatter("%(message)s"))
    root.addHandler(handler)
