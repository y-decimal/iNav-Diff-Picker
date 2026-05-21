import pytest
from pathlib import Path
from file_parser import FileParser
import tempfile

# Fixtures
test_dir = "tests/fixtures"


# Test cases


def test_file_parser_init():
    parser = FileParser(test_dir)
    assert parser.source_dir == Path(test_dir)
    assert parser.diff_files == []


def test_parse_files():
    parser = FileParser(test_dir)
    parser.parse_files()
    diff_files = parser.get_diff_files()
    assert len(diff_files) == 1
    assert diff_files[0].name == "INAV_9.0.1_cli_20260518_131434.txt"
