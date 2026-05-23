import json
from pathlib import Path


class DiffParser:

    first_valid_header = "# resources"
    invalid_headers = ["# restore original profile selection", "# save configuration"]

    def __init__(self, file_path):
        self.file_path = file_path
        self.diffs = []
        self.debugLevel = 0
        with open('header_categories.json', 'r') as f:
            self.header_mapping = json.load(f)

    def parse_diffs(self):
        with open(self.file_path, "r") as f:
            content = f.read()
            diff_block = []
            valid = False
            for line in content.splitlines():
                if (
                    not valid
                    and line.startswith("#")
                    and line.lower().strip() != DiffParser.first_valid_header
                ):
                    if self.debugLevel > 0:
                        print(
                            "--------------------- Found header before first valid header, skipping diff block ---------------------"
                        )
                    diff_block = []
                    continue
                elif (
                    not valid
                    and line.startswith("#")
                    and line.lower().strip() == DiffParser.first_valid_header
                ):
                    valid = True
                    if self.debugLevel > 0:
                        print(
                            "Found first valid header, starting to parse diffs      #",
                            len(self.diffs),
                            " :",
                            line,
                        )
                if line.startswith("#") and line.lower().strip() in [
                    h.lower() for h in DiffParser.invalid_headers
                ]:
                    if self.debugLevel > 0:
                        print(
                            "--------------------- Found invalid header, skipping diff block ---------------------"
                        )
                    if diff_block:
                        self.diffs.append(diff_block)
                        if self.debugLevel > 1:
                            print(
                                "Added diff block to diffs at index      #",
                                len(self.diffs) - 1,
                                " :",
                                diff_block[0],
                            )
                    diff_block = []
                    continue
                if line.startswith("#"):
                    if diff_block:
                        self.diffs.append(diff_block)
                        if self.debugLevel > 1:
                            print(
                                "Added diff block to diffs at index      #",
                                len(self.diffs) - 1,
                                " :",
                                diff_block[0],
                            )
                            print(
                                "------------------------ End diff block #",
                                len(self.diffs) - 1,
                                "------------------------",
                            )
                    diff_block = []
                    diff_block.append(line)
                    if self.debugLevel > 1:
                        print(
                            "Added header to current diff block      #",
                            len(self.diffs),
                            " :",
                            line,
                        )
                elif line.strip() == "":
                    if self.debugLevel > 2:
                        print(
                            "--------------------- Found empty line, skipping ---------------------"
                        )
                    continue
                elif diff_block:
                    diff_block.append(line)
                    if self.debugLevel > 3:
                        print(
                            "Added line to current diff block        #",
                            len(self.diffs),
                            " :",
                            line,
                        )

            # the diff file ends with an empty header line, so we do not need to add the last diff block

    def get_header_keywords(self):
        header_keywords = []
        for diff in self.diffs:
            if diff and diff[0].startswith("#") and diff[0] not in header_keywords:
                header_keywords.append(diff[0])

        return header_keywords

    def filter_diffs(self, header_keywords):
        filtered_diffs = []
        for diff in self.diffs:
            for header_keyword in header_keywords:
                if diff and diff[0].lower().strip() == header_keyword.lower().strip() and len(diff) > 1:
                    filtered_diffs.append(diff)
                    if self.debugLevel > 0:
                        print(
                            "Added diff block to filtered diffs      #",
                            len(filtered_diffs) - 1,
                            " :",
                            diff[0],
                        )
        return filtered_diffs

    def get_categories(self):
        categories = []
        for diff in self.diffs:
            if diff and diff[0].startswith("#"):
                category = self.get_category_for_header(diff[0])
                if category not in categories:
                    categories.append(category)
        return categories

    def get_category_for_header(self, header):
        header_lower = header.lower().strip()
        for category, headers in self.header_mapping['categories'].items():
            if any(h.lower() == header_lower for h in headers):
                return category
        return "uncategorized"
    
    def get_all_headers_with_category(self, category):
        headers = self.header_mapping['categories'].get(category, [])
        return headers

    def filter_diffs_by_category(self, category_keywords):
        filtered_diffs = []
        for diff in self.diffs:
            if diff and diff[0].startswith("#"):
                category = self.get_category_for_header(diff[0])
                if category in category_keywords and len(diff) > 1:
                    filtered_diffs.append(diff)
                    if self.debugLevel > 0:
                        print(
                            "Added diff block to filtered diffs by category      #",
                            len(filtered_diffs) - 1,
                            " :",
                            diff[0],
                            " (category: ",
                            category,
                            ")",
                        )
        return filtered_diffs

        


    def get_diffs(self):
        return self.diffs

       
