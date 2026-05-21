from pathlib import Path


class DiffParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.diffs = []

    def parse_diffs(self):
        with open(self.file_path, "r") as f:
            content = f.read()
            index = 0
            diff_block = []
            for line in content.splitlines():
                if line.startswith("#"):
                    if (diff_block):
                        self.diffs.append(diff_block)
                    diff_block = []
                    diff_block.append(line)
                elif line.strip() == "":
                    if diff_block:
                        self.diffs.append(diff_block)

    def get_diffs(self):
        return self.diffs
