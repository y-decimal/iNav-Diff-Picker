from source.model import diff_parser
from source.model.file_parser import FileParser
from source.model.diff_parser import DiffParser

class Model:
    def __init__(self):
        self.file_parser = FileParser()
        self.active_file = None


    def get_files(self, source_directory):
        self.file_parser.set_source_dir(source_directory)
        self.file_parser.parse_files()
        return self.file_parser.get_diff_files()
        
    def set_active_file(self, file_name):
        self.active_file = file_name

    def get_active_file_content(self):
        if not self.active_file:
            return None
    
        diff_parser = DiffParser(self.active_file)
        diff_parser.parse_diffs()
        return diff_parser.get_diffs()

    def get_list_of_categories(self):
        if not self.active_file:
            return None
        diff_parser = DiffParser(self.active_file)
        diff_parser.parse_diffs()
        # diff_parser.debugLevel = 1
        return diff_parser.get_categories()
    
    def get_category_content(self, category_name):
        if not self.active_file:
            return None
        diff_parser = DiffParser(self.active_file)
        diff_parser.parse_diffs()
        # diff_parser.debugLevel = 1
        return diff_parser.filter_diffs_by_category(category_name)
    