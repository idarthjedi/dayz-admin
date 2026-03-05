import re


def strip_codes(source: str) -> str:
    """Strip control characters (newline, tab) and whitespace from a string."""
    control_chars = ["\n", "\t"]
    for c in control_chars:
        source = source.strip(c)
    return source.strip()


def safe_filename(source: str) -> str:
    """Replace invalid filename characters with underscores."""
    invalid = r'<>:"/\|?* ,'
    for char in invalid:
        source = source.replace(char, "_")
    return source


def remove_notes(string: str) -> str:
    """Remove <<note>> markers from a string."""
    pattern = r"(<<.*>>)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(1) is not None:
            return ""

    return regex.sub(_replacer, string)


def remove_comments(string: str) -> str:
    """Remove // and /* */ comments while preserving quoted strings."""
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)

    return regex.sub(_replacer, string)
