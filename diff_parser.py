from pathlib import Path


class DiffParser:

    file_path = Path("")
    diffs = []
    debug = False

    def __init__(self, file_path):
        self.file_path = file_path
        self.diffs = []
        self.debug = False

    def parse_diffs(self):
        with open(self.file_path, "r") as f:
            content = f.read()
            diff_block = []
            for line in content.splitlines():
                if line.startswith("#"):
                    if diff_block:
                        self.diffs.append(diff_block)
                        if self.debug:
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
                    if self.debug:
                        print(
                            "Added header to current diff block      #",
                            len(self.diffs),
                            " :",
                            line,
                        )
                elif line.strip() == "":
                    if self.debug:
                        print(
                            "--------------------- Found empty line, skipping ---------------------"
                        )
                    continue
                elif diff_block:
                    diff_block.append(line)
                    if self.debug:
                        print(
                            "Added line to current diff block        #",
                            len(self.diffs),
                            " :",
                            line,
                        )

            # the diff file ends with an empty header line, so we do not need to add the last diff block

    def filter_diffs(self, header_keywords):
        filtered_diffs = []
        for diff in self.diffs:
            if diff and diff[0].lower().strip() in header_keywords.lower().strip():
                filtered_diffs.append(diff)
                if self.debug:
                    print("Added diff block to filtered diffs      #", len(filtered_diffs) - 1, " :", diff[0])
        return filtered_diffs

    def get_diffs(self):
        return self.diffs
