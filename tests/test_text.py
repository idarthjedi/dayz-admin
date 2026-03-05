from dayz_admin_tools.utilities.text import (
    remove_comments,
    remove_notes,
    safe_filename,
    strip_codes,
)


class TestStripCodes:
    def test_strips_newlines(self):
        assert strip_codes("\nhello\n") == "hello"

    def test_strips_tabs(self):
        assert strip_codes("\thello\t") == "hello"

    def test_strips_mixed(self):
        assert strip_codes("\n\t  hello  \t\n") == "hello"

    def test_empty_string(self):
        assert strip_codes("") == ""

    def test_preserves_internal_spaces(self):
        assert strip_codes("hello world") == "hello world"


class TestSafeFilename:
    def test_replaces_spaces(self):
        assert safe_filename("hello world") == "hello_world"

    def test_replaces_special_chars(self):
        assert safe_filename('file<>:"/\\|?*name') == "file_________name"

    def test_replaces_commas(self):
        assert safe_filename("a,b,c") == "a_b_c"

    def test_clean_string_unchanged(self):
        assert safe_filename("clean_name") == "clean_name"


class TestRemoveNotes:
    def test_removes_notes(self):
        assert remove_notes("hello <<note>> world") == "hello  world"

    def test_no_notes(self):
        assert remove_notes("hello world") == "hello world"

    def test_multiple_notes(self):
        # remove_notes uses greedy regex, so <<a>> text <<b>> matches as one group
        assert remove_notes("<<a>> text <<b>>") == ""


class TestRemoveComments:
    def test_removes_single_line_comment(self):
        result = remove_comments("code // comment")
        assert result.strip() == "code"

    def test_preserves_quoted_strings(self):
        result = remove_comments('"hello // world"')
        assert result == '"hello // world"'

    def test_removes_multiline_comment(self):
        result = remove_comments("code /* comment */ more")
        assert result == "code  more"

    def test_no_comments(self):
        assert remove_comments("just code") == "just code"
