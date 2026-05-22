import pytest
from pathlib import Path
from diff_parser import DiffParser

# Fixtures

test_file_valid = "tests/fixtures/INAV_9.0.1_cli_20260518_131434.txt"
test_file_invalid = "tests/fixtures/not_a_diff.txt"

# Test cases

def test_diff_parser_init():
    parser = DiffParser(test_file_valid)
    assert parser.file_path == test_file_valid
    assert parser.diffs == []
    
def test_parse_diffs_valid_file():
    parser = DiffParser(test_file_valid)
    parser.parse_diffs()
    diffs = parser.get_diffs()
    assert len(diffs) > 0
    assert len(diffs[0]) > 0
    assert diffs[0][0].startswith("#")
    assert "version" in diffs[0][0].lower()
    
    assert len(diffs) > 10, "Expected multiple diff blocks in the file"
    
    found_servo_diff = False
    found_servo_content = False
    for diff in diffs:
        assert diff[0].startswith("#")
        if ("# outputs [servo]" in diff[0].lower().strip()):
            found_servo_diff = True
        for line in diff[1:]:
            assert not line.startswith("#")
            if ("servo 2 1100 1900 1500 100" in line.lower().strip()):
                found_servo_content = True
    
    assert found_servo_diff, "Expected to find a diff block for servo outputs"
    assert found_servo_content, "Expected to find specific servo output content in the diffs"




def test_parse_diffs_invalid_file():
    parser = DiffParser(test_file_invalid)
    parser.parse_diffs()
    diffs = parser.get_diffs()
    assert len(diffs) == 0
    