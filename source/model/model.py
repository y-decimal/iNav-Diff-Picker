from source.model.file_parser import FileParser

class Model:
    def __init__(self):
        self.file_parser = FileParser()


    def get_files(self, source_directory):
        self.file_parser.set_source_dir(source_directory)
        self.file_parser.parse_files()
        return self.file_parser.get_diff_files()
        