from pathlib import Path

save_append = ["# save configuration", "save", "", "#"]


class DiffMerger:

    diff_lists = []
    merged_list = []
    output_dir = Path("")

    def __init__(self, output_dir, diff_lists):
        self.output_dir = Path(output_dir)
        self.diff_lists = diff_lists

    def merge_diffs(self):
        self.merged_list = self.diff_lists.copy()  # ← Create a copy, not a reference
        self.merged_list.append(save_append)

    def save_merged_diffs(self, output_file_name):
        self.merge_diffs()
        output_path = self.output_dir / output_file_name
        with open(output_path, "w") as f:
            for diff in self.merged_list:
                f.write("\n".join(diff))
                f.write("\n\n")  # Add empty line between diff blocks in output file
