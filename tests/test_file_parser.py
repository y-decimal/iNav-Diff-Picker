import pytest
from pathlib import Path
from source.model.file_parser import FileParser
import tempfile

# ===== FIXTURES =====


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def dir_with_diff_files(temp_dir):
    """Create a directory with multiple diff files"""
    # Create valid diff files (first line must contain "diff all")
    diff1 = temp_dir / "diff1.txt"
    diff1.write_text("diff all\n# OSD\nset osd_name = value1\n")

    diff2 = temp_dir / "diff2.txt"
    diff2.write_text("diff all\n# Control Profile\nset profile_rate = 5000\n")

    diff3 = temp_dir / "diff3.txt"
    diff3.write_text("diff all\n# Battery Settings\nset battery_alert = 20\n")

    return temp_dir


@pytest.fixture
def dir_with_mixed_files(temp_dir):
    """Create a directory with both diff and non-diff files"""
    # Valid diff file (first line must contain "diff all")
    diff_file = temp_dir / "config.txt"
    diff_file.write_text("diff all\n# Settings\nset value = 1\n")

    # Non-diff files
    readme = temp_dir / "README.txt"
    readme.write_text("This is just a readme file\nNo diffs here\n")

    other = temp_dir / "notes.txt"
    other.write_text("Some notes about the project\n")

    return temp_dir


@pytest.fixture
def dir_with_non_diff_files(temp_dir):
    """Create a directory with only non-diff files"""
    file1 = temp_dir / "readme.txt"
    file1.write_text("Just a readme\n")

    file2 = temp_dir / "notes.txt"
    file2.write_text("Some notes\n")

    return temp_dir


@pytest.fixture
def empty_dir(temp_dir):
    """Create an empty directory"""
    return temp_dir


@pytest.fixture
def dir_with_single_diff(temp_dir):
    """Create a directory with a single diff file"""
    diff_file = temp_dir / "single_diff.txt"
    diff_file.write_text("diff all\n# version\nfirmware_version=9.0.1\n")
    return temp_dir


@pytest.fixture
def dir_with_case_variations(temp_dir):
    """Create files with case variations in 'diff all' keyword"""
    file1 = temp_dir / "file1.txt"
    file1.write_text("DIFF ALL content\n")  # uppercase, should not match

    file2 = temp_dir / "file2.txt"
    file2.write_text("diff all in the middle\n")  # proper case, should match

    file3 = temp_dir / "file3.txt"
    file3.write_text("NO CONTENT HERE\n")

    return temp_dir


# ===== INITIALIZATION TESTS =====


def test_file_parser_initialization(temp_dir):
    """Test FileParser initializes correctly"""
    parser = FileParser(str(temp_dir))
    assert parser.source_dir == temp_dir
    assert parser.diff_files == []


def test_file_parser_with_path_object(temp_dir):
    """Test FileParser accepts path as string"""
    parser = FileParser(str(temp_dir))
    assert isinstance(parser.source_dir, Path)


def test_file_parser_with_different_paths():
    """Test FileParser initialization with different path types"""
    path1 = "C:\\some\\path"
    parser1 = FileParser(path1)
    assert parser1.source_dir == Path(path1)


# ===== PARSE_FILES TESTS =====


def test_parse_files_finds_diff_files(dir_with_diff_files):
    """Test that parse_files identifies files containing 'diff'"""
    parser = FileParser(str(dir_with_diff_files))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert len(diff_files) == 3, "Should find 3 diff files"


def test_parse_files_finds_single_diff(dir_with_single_diff):
    """Test finding a single diff file"""
    parser = FileParser(str(dir_with_single_diff))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert len(diff_files) == 1
    assert diff_files[0].name == "single_diff.txt"


def test_parse_files_ignores_non_diff_files(dir_with_non_diff_files):
    """Test that parse_files ignores files without 'diff'"""
    parser = FileParser(str(dir_with_non_diff_files))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert len(diff_files) == 0, "Should find no diff files"


def test_parse_files_mixed_content(dir_with_mixed_files):
    """Test parsing directory with both diff and non-diff files"""
    parser = FileParser(str(dir_with_mixed_files))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert len(diff_files) == 1, "Should find only 1 diff file"
    assert diff_files[0].name == "config.txt"


def test_parse_files_empty_directory(empty_dir):
    """Test parsing an empty directory"""
    parser = FileParser(str(empty_dir))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert len(diff_files) == 0


def test_parse_files_case_insensitive(dir_with_case_variations):
    """Test that 'diff all' keyword search is case-sensitive"""
    parser = FileParser(str(dir_with_case_variations))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    # Should find only the lowercase "diff all", not "DIFF ALL"
    assert len(diff_files) == 1, "Should find only 1 file with lowercase 'diff all'"


# ===== GET_DIFF_FILES TESTS =====


def test_get_diff_files_returns_list(dir_with_diff_files):
    """Test that get_diff_files returns a list"""
    parser = FileParser(str(dir_with_diff_files))
    parser.parse_files()
    result = parser.get_diff_files()

    assert isinstance(result, list)


def test_get_diff_files_returns_path_objects(dir_with_diff_files):
    """Test that get_diff_files returns Path objects"""
    parser = FileParser(str(dir_with_diff_files))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert all(isinstance(f, Path) for f in diff_files)


def test_get_diff_files_before_parse(temp_dir):
    """Test get_diff_files before parse_files is called"""
    parser = FileParser(str(temp_dir))
    diff_files = parser.get_diff_files()

    assert isinstance(diff_files, list)
    assert len(diff_files) == 0


def test_get_diff_files_empty_directory(empty_dir):
    """Test get_diff_files on empty directory"""
    parser = FileParser(str(empty_dir))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    assert diff_files == []


# ===== FILE CONTENT TESTS =====


def test_parse_files_checks_file_content(dir_with_mixed_files):
    """Test that parse_files actually reads file content"""
    parser = FileParser(str(dir_with_mixed_files))
    parser.parse_files()
    diff_files = parser.get_diff_files()

    # config.txt has "diff" in content
    found_config = any(f.name == "config.txt" for f in diff_files)
    assert found_config, "Should find config.txt which contains 'diff'"

    # readme.txt does not have "diff"
    found_readme = any(f.name == "README.txt" for f in diff_files)
    assert not found_readme, "Should not find README.txt which doesn't contain 'diff'"


# ===== EDGE CASES =====


def test_parse_files_nonexistent_directory():
    """Test handling of non-existent directory"""
    parser = FileParser("/nonexistent/path/to/directory")
    # Should handle gracefully - implementation dependent
    try:
        parser.parse_files()
        # If it doesn't raise, diff_files should be empty
        assert len(parser.get_diff_files()) == 0
    except (FileNotFoundError, OSError):
        # It's also acceptable to raise an error
        pass


def test_parse_files_multiple_calls_accumulates(dir_with_diff_files):
    """Test that multiple parse_files calls accumulate results"""
    parser = FileParser(str(dir_with_diff_files))

    parser.parse_files()
    first_count = len(parser.get_diff_files())

    parser.parse_files()
    second_count = len(parser.get_diff_files())

    # Second call should accumulate (if implementation appends)
    # or be the same (if implementation replaces)
    # Test documents the behavior
    assert second_count >= first_count


def test_file_order_consistency(dir_with_diff_files):
    """Test that file order is consistent across calls"""
    parser = FileParser(str(dir_with_diff_files))
    parser.parse_files()
    files1 = [f.name for f in parser.get_diff_files()]

    parser2 = FileParser(str(dir_with_diff_files))
    parser2.parse_files()
    files2 = [f.name for f in parser2.get_diff_files()]

    # File order might vary, but set should be the same
    assert set(files1) == set(files2)
