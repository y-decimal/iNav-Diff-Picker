from file_parser import FileParser
from diff_parser import DiffParser
from diff_merger import DiffMerger
from pathlib import Path

source_directory = "source_diffs"
output_directory = "output_diffs"


def main():
    file_parser = FileParser(source_directory)
    file_parser.parse_files()
    diff_files = file_parser.get_diff_files()

    count = len(diff_files)
    plural = "file" if count == 1 else "files"
    print(f"Found {count} diff {plural} in the source directory.")

    diff_parsers = []

    for diff_file in diff_files:
        print(f"Parsing diff file: {diff_file.name}")
        diff_parser = DiffParser(diff_file)
        diff_parser.parse_diffs()
        diffs = diff_parser.get_diffs()
        diff_parsers.append(diff_parser)
        print(f"Found {len(diffs)} diffs in {diff_file.name}.")

    diffs = []

    for diff_parser in diff_parsers:
        diffs.extend(diff_parser.get_diffs())

    diff_merger = DiffMerger(output_directory, diffs)
    diff_merger.save_merged_diffs("merged_diffs.txt")
    print(f"Merged diffs saved to {output_directory}/merged_diffs.txt")

    filter_keywords = []

    for diff_parser in diff_parsers:
        header_keywords = diff_parser.get_header_keywords()
        print(f"Header keywords in {diff_parser.file_path.name}: {header_keywords}")
        filter_keywords.extend(header_keywords)

    filtered_diffs = []

    for diff_parser in diff_parsers:
        print(f"Filtering diffs in file: {diff_parser.file_path.name}")
        for keyword in filter_keywords:
            print(f"Filtering with keyword: {keyword}")
        diff_parser.debugLevel = 1
        filtered_diffs.extend(diff_parser.filter_diffs(filter_keywords))
        print(
            f"Found {len(filtered_diffs)} diffs matching filter keywords in {diff_parser.file_path.name}."
        )

    filtered_diff_merger = DiffMerger(output_directory, filtered_diffs)
    filtered_diff_merger.save_merged_diffs("filtered_diffs.txt")
    print(f"Merged diffs saved to {output_directory}/filtered_diffs.txt")


if __name__ == "__main__":
    main()
