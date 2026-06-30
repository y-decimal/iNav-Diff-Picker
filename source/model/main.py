from source.model.file_parser import FileParser
from source.model.diff_parser import DiffParser
from source.model.diff_merger import DiffMerger
from pathlib import Path

source_directory = "source_diffs"
output_directory = "output_diffs"


def main():
    file_parser = FileParser()
    file_parser.set_source_dir(source_directory)
    file_parser.parse_files()
    diff_files = file_parser.get_diff_files()

    count = len(diff_files)
    plural = "file" if count == 1 else "files"
    print(f"Found {count} diff {plural} in the source directory.")

    if count == 0:
        print("No diff files found.")
        return

    selected_file = Path("")

    if count == 1:
        selected_file = diff_files[0]

    elif count > 1:
        print("Select a diff file to merge by entering the corresponding number: ")
        for i, diff_file in enumerate(diff_files):
            print(f"{i + 1}. {diff_file.name}")
        while True:
            try:
                selection = int(input("Enter the number of the diff file to merge: "))
                if 1 <= selection <= len(diff_files):
                    selected_file = diff_files[selection - 1]
                    print(f"You selected: {selected_file.name}")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(diff_files)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    print(f"Parsing diff file: {selected_file.name}")
    diff_parser = DiffParser(selected_file)
    diff_parser.parse_diffs()
    diffs = diff_parser.get_diffs()
    categories = diff_parser.get_categories()
    print(f"Found {len(diffs)} diffs in {selected_file.name}.")

    filter_list = []

    main_cli(filter_list, diff_parser, categories)

    diff_merger = DiffMerger(output_directory, filter_list)

    print("Choose file name for merged diffs (without extension): ")
    file_name = input("Enter file name: ") + ".txt"
    diff_merger.save_merged_diffs(file_name)


def main_cli(filter_list, diff_parser, categories):
    print("Choose category:")
    while True:
        print("0. All categories")
        idx = 1
        for i, category in enumerate(categories):
            print(f"{i + 1}. {category}")
            idx += 1
        print(f"{idx}. Merge selected diffs and exit")
        print(f"{idx+1}. Exit without merging")
        print(
            "Current selection:",
            [diff[0] for diff in filter_list],
        )
        try:
            selection = int(input("Enter a number: "))
            if selection == 0:
                filter_list.extend(
                    diff_selection(
                        diff_parser,
                        diff_parser.get_diffs(),
                    )
                )
                continue
            if selection <= len(categories) and selection > 0:
                filter_list.extend(
                    diff_selection(
                        diff_parser,
                        diff_parser.filter_diffs_by_category(categories[selection - 1]),
                    )
                )
                continue
            elif selection == idx:
                # Merge selected diffs and exit
                break
            elif selection == idx + 1:
                # Exit without merging
                exit()

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


def diff_selection(diff_parser, filtered_diffs):
    selected_diff = []
    while True:
        print("Select a diff to merge by entering the corresponding number: ")
        for i, diff in enumerate(filtered_diffs):
            print(f"{i + 1}. {diff[0]}")
        print(f"{len(filtered_diffs) + 1}. Reset selection")
        print(f"{len(filtered_diffs) + 2}. Exit")
        print(f"Current selection: {[diff[0] for diff in selected_diff]}")
        try:
            selection = int(input("Enter the number of the diff to merge: "))
            if 1 <= selection <= len(filtered_diffs):
                selected_diff.append(filtered_diffs[selection - 1])
                print(f"You selected: {filtered_diffs[selection - 1][0]}")
                continue
            elif selection == len(filtered_diffs) + 1:
                selected_diff = []
                print("Selection reset.")
            elif selection == len(filtered_diffs) + 2:
                break
            else:
                print(f"Please enter a number between 1 and {len(filtered_diffs)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return selected_diff


def print_filtered_diff_headers(diff_parser, categories):

    filtered_diffs = diff_parser.filter_diffs_by_category(categories)
    if not filtered_diffs:
        print("No diffs match the selected category.")
    else:
        print(f"Diffs in category '{categories}':")
        for diff in filtered_diffs:
            print(diff[0])


if __name__ == "__main__":
    main()
