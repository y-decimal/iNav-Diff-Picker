from pathlib import Path

class FileParser:
    
    diff_files = list()
    source_dir = Path("")
    
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)

    def parse_files(self):
        txt_files = list(self.source_dir.glob("*.txt"))
        for txt_file in txt_files:
            with open(txt_file, "r") as f:
                content = f.read()
                if "diff all" in content.splitlines()[0]:
                    print(f"Found diff in {txt_file.name}")
                    self.diff_files.append(txt_file)

    def get_diff_files(self):
        return self.diff_files