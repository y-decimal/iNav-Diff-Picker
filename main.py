from file_parser import FileParser
from diff_parser import DiffParser

source_directory = "source_diffs"

filter_keywords = ["# geozone", "# safehome", "# Modes [aux]"]


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

    for diff_parser in diff_parsers:
        print(f"Filtering diffs in file: {diff_parser.file_path.name}")
        filtered_diffs = diff_parser.filter_diffs(filter_keywords)
        print(
            f"Found {len(filtered_diffs)} diffs matching filter keywords in {diff_parser.file_path.name}."
        )


if __name__ == "__main__":
    main()
