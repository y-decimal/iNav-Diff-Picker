import pytest
from pathlib import Path
import tempfile
from diff_merger import DiffMerger


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_diff_lists():
    """Sample diff blocks to merge"""
    return [
        ["# OSD", "set osd_name = value1", "set osd_size = 10"],
        ["# Control Profile", "set profile_rate = 5000", "set profile_expo = 1.5"],
        ["# Rates", "set rate_roll = 45", "set rate_pitch = 45"],
    ]


@pytest.fixture
def single_diff_list():
    """Single diff block"""
    return [
        ["# OSD", "set osd_name = value1"],
    ]


@pytest.fixture
def empty_diff_lists():
    """Empty diff lists"""
    return []


# ===== INITIALIZATION TESTS =====


def test_diff_merger_initialization(temp_dir, sample_diff_lists):
    """Test that DiffMerger initializes correctly"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)

    assert merger.output_dir == temp_dir
    assert merger.diff_lists == sample_diff_lists
    assert merger.merged_list == []


def test_diff_merger_with_different_path(sample_diff_lists):
    """Test initialization with different path"""
    test_path = "C:\\some\\path"
    merger = DiffMerger(test_path, sample_diff_lists)

    assert merger.output_dir == Path(test_path)


# ===== MERGE_DIFFS TESTS =====


def test_merge_diffs_combines_lists(temp_dir, sample_diff_lists):
    """Test that merge_diffs combines all diff lists"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    merger.merge_diffs()

    # Should have all original diffs plus save_append
    assert len(merger.merged_list) == len(sample_diff_lists) + 1


def test_merge_diffs_adds_save_append(temp_dir, sample_diff_lists):
    """Test that merge_diffs appends save configuration block"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    merger.merge_diffs()

    # Last item should be save_append
    assert merger.merged_list[-1] == ["# save configuration", "save", "", "#"]


def test_merge_diffs_preserves_order(temp_dir, sample_diff_lists):
    """Test that original diff order is preserved"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    merger.merge_diffs()

    # First three should match original order
    for i in range(len(sample_diff_lists)):
        assert merger.merged_list[i] == sample_diff_lists[i]


def test_merge_diffs_single_list(temp_dir, single_diff_list):
    """Test merge_diffs with single diff block"""
    merger = DiffMerger(str(temp_dir), single_diff_list)
    merger.merge_diffs()

    assert len(merger.merged_list) == 2  # 1 diff + save_append
    assert merger.merged_list[0] == single_diff_list[0]


def test_merge_diffs_empty_lists(temp_dir, empty_diff_lists):
    """Test merge_diffs with empty lists"""
    merger = DiffMerger(str(temp_dir), empty_diff_lists)
    merger.merge_diffs()

    # Should only have save_append
    assert len(merger.merged_list) == 1
    assert merger.merged_list[0] == ["# save configuration", "save", "", "#"]


# ===== SAVE_MERGED_DIFFS TESTS =====


def test_save_merged_diffs_creates_file(temp_dir, sample_diff_lists):
    """Test that save_merged_diffs creates output file"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    output_file = "merged_output.txt"

    merger.save_merged_diffs(output_file)

    output_path = temp_dir / output_file
    assert output_path.exists()
    assert output_path.is_file()


def test_save_merged_diffs_file_content(temp_dir, sample_diff_lists):
    """Test that output file has correct content"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    output_file = "output.txt"

    merger.save_merged_diffs(output_file)

    output_path = temp_dir / output_file
    content = output_path.read_text()

    # Check that all diff content is in the file
    assert "# OSD" in content
    assert "# Control Profile" in content
    assert "# Rates" in content
    assert "# save configuration" in content
    assert "save" in content


def test_save_merged_diffs_formatting(temp_dir, single_diff_list):
    """Test that output file is properly formatted"""
    merger = DiffMerger(str(temp_dir), single_diff_list)
    output_file = "formatted_output.txt"

    merger.save_merged_diffs(output_file)

    output_path = temp_dir / output_file
    content = output_path.read_text()

    # Should have double newlines between blocks
    assert "\n\n" in content


def test_save_merged_diffs_calls_merge_diffs(temp_dir, sample_diff_lists):
    """Test that save_merged_diffs calls merge_diffs"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)

    # merged_list should be empty before calling
    assert len(merger.merged_list) == 0

    merger.save_merged_diffs("output.txt")

    # merged_list should be populated after calling
    assert len(merger.merged_list) > 0


def test_save_merged_diffs_with_custom_filename(temp_dir, sample_diff_lists):
    """Test save_merged_diffs with different filenames"""
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    filenames = ["custom1.txt", "custom2.txt", "merged.txt"]

    for filename in filenames:
        merger.save_merged_diffs(filename)
        output_path = temp_dir / filename
        assert output_path.exists()


def test_save_merged_diffs_empty_diffs(temp_dir, empty_diff_lists):
    """Test save_merged_diffs with empty diff lists"""
    merger = DiffMerger(str(temp_dir), empty_diff_lists)
    output_file = "empty_output.txt"

    merger.save_merged_diffs(output_file)

    output_path = temp_dir / output_file
    content = output_path.read_text()

    # Should still contain save_append
    assert "# save configuration" in content


def test_save_merged_diffs_overwrites_existing_file(temp_dir, sample_diff_lists):
    """Test that save_merged_diffs overwrites existing files"""
    output_file = "overwrite_test.txt"
    output_path = temp_dir / output_file

    # Create initial file
    output_path.write_text("Original content")
    assert "Original content" in output_path.read_text()

    # Save merged diffs
    merger = DiffMerger(str(temp_dir), sample_diff_lists)
    merger.save_merged_diffs(output_file)

    # Content should be replaced
    content = output_path.read_text()
    assert "Original content" not in content
    assert "# OSD" in content
