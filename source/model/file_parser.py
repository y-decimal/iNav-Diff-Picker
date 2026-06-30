from pathlib import Path


class FileParser:

    def __init__(self):
        self.diff_files = []
        self.debug = False
        self.source_dir = Path("")

    def set_source_dir(self, source_dir):
        self.source_dir = Path(source_dir)

    def parse_files(self):
        
        if (self.source_dir == Path("")):
            print("No source directory provided. Please provide a valid source directory.")
            return
        
        txt_files = list(self.source_dir.glob("*.txt"))
        
        for txt_file in txt_files:
            with open(txt_file, "r") as f:
                content = f.read()
                if "diff all" in content.splitlines()[0]:
                    self.diff_files.append(txt_file)
                    if self.debug:
                        print(f"Found diff in {txt_file}")

    def get_diff_files(self):
        return self.diff_files
