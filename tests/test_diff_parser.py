import pytest
from pathlib import Path
import tempfile
from source.model.diff_parser import DiffParser

# ===== FIXTURES =====


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def valid_diff_file(temp_dir):
    """Create a valid diff file with multiple headers"""
    content = """# version
firmware_version=9.0.1

# resources

# outputs [servo]
servo 0 1000 2000 1500 50
servo 1 1100 1900 1500 100
servo 2 1100 1900 1500 100

# safehome
safehome 0 48.123 -122.456 100 0 0 0

# battery
battery_meter_alert=20
battery_meter_warn=30

# board
board_name=MATEKF411

#
"""
    file_path = temp_dir / "valid_diff.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def empty_file(temp_dir):
    """Create an empty file"""
    file_path = temp_dir / "empty.txt"
    file_path.write_text("")
    return file_path


@pytest.fixture
def file_without_headers(temp_dir):
    """Create a file without any headers"""
    content = """Just some regular content
No headers here
No diffs either
"""
    file_path = temp_dir / "no_headers.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def file_with_empty_headers(temp_dir):
    """Create a file with empty header blocks"""
    content = """# resources

# header1

# header2

# header3
value1
value2
"""
    file_path = temp_dir / "empty_headers.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_diff_blocks():
    """Sample diff blocks for testing filter_diffs"""
    return [
        ["# outputs [servo]", "servo 0 1000 2000 1500 50"],
        ["# safehome", "safehome 0 48.123 -122.456 100 0"],
        ["# battery", "battery_meter_alert=20"],
        ["# board", "board_name=MATEKF411"],
    ]


@pytest.fixture
def file_with_invalid_headers(temp_dir):
    """Create a file with some invalid headers that should be skipped"""
    content = """diff all

# version
# INAV/SPEEDYBEEF405WING 9.0.1 Apr 28 2026 / 18:03:52 (ed3f5c1e) 
# GCC-13.2.1 20231009

# start the command batch
batch start

# reset configuration to default settings
defaults noreboot

# resources

# Outputs [servo]
servo 1 1100 1900 1500 -100
servo 2 1100 1900 1500 100
servo 3 1000 2000 1000 100
    
# restore original profile selection

# save configuration
save

#
 
"""
    file_path = temp_dir / "invalid_headers.txt"
    file_path.write_text(content)
    return file_path


# ===== INITIALIZATION TESTS =====


def test_diff_parser_init(valid_diff_file):
    """Test DiffParser initialization"""
    parser = DiffParser(str(valid_diff_file))
    assert parser.file_path == str(valid_diff_file)
    assert parser.diffs == []
    assert parser.debugLevel == 0


# ===== PARSE_DIFFS TESTS =====


def test_parse_diffs_valid_file(valid_diff_file):
    """Test parsing a valid diff file"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    assert len(diffs) > 0, "Expected diffs to be parsed"
    assert len(diffs[0]) > 0, "Expected first diff block to have content"
    assert diffs[0][0].startswith("#"), "Expected header to start with #"


def test_parse_diffs_creates_blocks(valid_diff_file):
    """Test that parse_diffs creates correct number of blocks"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    # Should have 5 blocks: resources, servo, safehome, battery, board
    assert len(diffs) == 5, f"Expected 5 diff blocks, got {len(diffs)}"


def test_parse_diffs_block_headers(valid_diff_file):
    """Test that each block has correct header"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    expected_headers = [
        "# resources",
        "# outputs [servo]",
        "# safehome",
        "# battery",
        "# board",
    ]

    for i, expected in enumerate(expected_headers):
        assert (
            diffs[i][0] == expected
        ), f"Expected header '{expected}', got '{diffs[i][0]}'"


def test_parse_diffs_block_content(valid_diff_file):
    """Test that blocks contain expected content lines"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    # Check servo block (index 1) has servo lines
    servo_block = diffs[1]
    assert len(servo_block) > 1, "Servo block should have header + content"
    assert any(
        "servo" in line for line in servo_block[1:]
    ), "Servo block should contain servo lines"


def test_parse_diffs_empty_file(empty_file):
    """Test parsing an empty file"""
    parser = DiffParser(str(empty_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    assert len(diffs) == 0, "Empty file should result in no diffs"


def test_parse_diffs_no_headers(file_without_headers):
    """Test parsing file without headers"""
    parser = DiffParser(str(file_without_headers))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    assert len(diffs) == 0, "File without headers should result in no diffs"


def test_parse_diffs_empty_headers(file_with_empty_headers):
    """Test parsing file with empty header blocks"""
    parser = DiffParser(str(file_with_empty_headers))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    # Should still parse the headers
    assert len(diffs) >= 1, "Should parse at least one header"
    for diff in diffs:
        assert diff[0].startswith("#"), "Each block should start with a header"


def test_parse_diffs_multiple_calls(valid_diff_file):
    """Test that calling parse_diffs multiple times appends"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    first_count = len(parser.get_diffs())

    # Parse again (this will append to existing diffs)
    parser.parse_diffs()
    second_count = len(parser.get_diffs())

    # Should have double the diffs
    assert second_count == first_count * 2, "Multiple parse calls should append diffs"
    
def test_parse_diffs_invalid_headers(file_with_invalid_headers):
    """Test that invalid headers are skipped and do not create diff blocks"""
    parser = DiffParser(str(file_with_invalid_headers))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    expected_valid_headers = [
        "# resources",
        "# outputs [servo]",
    ]

    # Should only have 2 valid blocks: resources and servo
    assert len(diffs) == 2, f"Expected 2 valid diff blocks, got {len(diffs)}. Diffs: {diffs}"
    
    for i in range(len(diffs)):
        assert diffs[i][0].lower().strip() == expected_valid_headers[i].lower().strip(), f"Unexpected header '{diffs[i][0]}' found"
    
    for diff in diffs:
        assert diff[0].lower().strip() not in [h.lower() for h in DiffParser.invalid_headers], f"Invalid header '{diff[0]}' should be skipped"



# ===== GET_DIFFS TESTS =====


def test_get_diffs_returns_list(valid_diff_file):
    """Test that get_diffs returns a list"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    assert isinstance(diffs, list), "get_diffs should return a list"


def test_get_diffs_returns_same_as_internal(valid_diff_file):
    """Test that get_diffs returns the same list as internal diffs"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    diffs = parser.get_diffs()

    assert diffs is parser.diffs, "get_diffs should return the internal diffs list"


# ===== FILTER_DIFFS TESTS =====


def test_filter_diffs_basic(valid_diff_file):
    """Test filtering diffs by keyword"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    filtered = parser.filter_diffs_by_header(["# outputs [servo]"])

    assert len(filtered) == 1, "Should find 1 matching diff"
    assert filtered[0][0] == "# outputs [servo]"


def test_filter_diffs_multiple_keywords(valid_diff_file):
    """Test filtering with multiple keywords"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    filtered = parser.filter_diffs_by_header(["# outputs [servo]", "# safehome", "# battery"])

    assert len(filtered) == 3, f"Should find 3 matching diffs, got {len(filtered)}"


def test_filter_diffs_case_insensitive(valid_diff_file):
    """Test that filtering is case-insensitive"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    filtered = parser.filter_diffs_by_header(["# OUTPUTS [SERVO]"])

    assert len(filtered) == 1, "Filter should be case-insensitive"
    assert filtered[0][0] == "# outputs [servo]"


def test_filter_diffs_whitespace_tolerant(valid_diff_file):
    """Test that filtering tolerates extra whitespace"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    filtered = parser.filter_diffs_by_header(["  # outputs [servo]  "])

    assert len(filtered) == 1, "Filter should strip whitespace"


def test_filter_diffs_no_matches():
    """Test filtering with non-matching keywords"""
    parser = DiffParser("dummy_path")
    parser.diffs = [
        ["# outputs [servo]", "servo 0 1000 2000"],
        ["# battery", "battery_alert=20"],
    ]
    filtered = parser.filter_diffs_by_header(["# nonexistent", "# nothere"])

    assert len(filtered) == 0, "Should find no matching diffs"


def test_filter_diffs_partial_match_not_found():
    """Test that partial matches don't match"""
    parser = DiffParser("dummy_path")
    parser.diffs = [
        ["# outputs [servo]", "servo 0 1000 2000"],
    ]
    # Partial match should not work
    filtered = parser.filter_diffs_by_header(["# outputs"])

    assert len(filtered) == 0, "Partial matches should not be found"


def test_filter_diffs_empty_diffs():
    """Test filtering when no diffs have been parsed"""
    parser = DiffParser("dummy_path")
    filtered = parser.filter_diffs_by_header(["# outputs [servo]"])

    assert len(filtered) == 0, "Filtering empty diffs should return empty list"


def test_filter_diffs_returns_list_of_blocks(valid_diff_file):
    """Test that filter_diffs returns complete diff blocks"""
    parser = DiffParser(str(valid_diff_file))
    parser.parse_diffs()
    filtered = parser.filter_diffs_by_header(["# safehome"])

    assert len(filtered) == 1
    assert filtered[0][0] == "# safehome"
    assert len(filtered[0]) > 1, "Should include full block with header and content"


# ===== DEBUG LEVEL TESTS =====


def test_debug_level_default(valid_diff_file):
    """Test that debug level is 0 by default"""
    parser = DiffParser(str(valid_diff_file))
    assert parser.debugLevel == 0


def test_debug_level_setting(valid_diff_file):
    """Test that debug level can be changed"""
    parser = DiffParser(str(valid_diff_file))
    parser.debugLevel = 2
    parser.parse_diffs()  # Should execute without errors

    assert parser.debugLevel == 2
    assert len(parser.get_diffs()) > 0


# ===== EDGE CASES =====


def test_parse_diffs_file_not_found():
    """Test handling of non-existent file"""
    parser = DiffParser("/nonexistent/path/to/file.txt")
    with pytest.raises(FileNotFoundError):
        parser.parse_diffs()


def test_filter_diffs_empty_keyword_list():
    """Test filtering with empty keyword list"""
    parser = DiffParser("dummy_path")
    parser.diffs = [["# outputs [servo]", "servo 0 1000 2000"]]
    filtered = parser.filter_diffs_by_header([])

    assert len(filtered) == 0, "Empty keyword list should return no results"
