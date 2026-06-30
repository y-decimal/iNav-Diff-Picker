from source.model import diff_parser
from source.model.file_parser import FileParser
from source.model.diff_parser import DiffParser

class Model:
    def __init__(self):
        self.file_parser = FileParser()
        self.diff_parser = None
        self.active_file = None
        
        self.content = []
        self.categories = []
        self.header_by_category = {}
        self.content_by_header = {}

    def get_files(self, source_directory):
        self.file_parser.set_source_dir(source_directory)
        self.file_parser.parse_files()
        return self.file_parser.get_diff_files()
        
    def set_active_file(self, file_name):
        self.active_file = file_name
        self.diff_parser = DiffParser(self.active_file)
        self.diff_parser.parse_diffs()
        
        self.content = self.diff_parser.get_diffs()
        self.categories = self.diff_parser.get_categories()
        self.header_by_category = {}
        self.content_by_header = {}
        
        for category in self.categories:
            self.header_by_category[category] = self.diff_parser.get_all_headers_with_category(category)
        
        for headers in self.header_by_category.values():
            for header in headers:
                self.content_by_header[header] = self.diff_parser.filter_diffs_by_header([header])

    def get_active_file_content(self):
        return self.content

    def get_list_of_categories(self):
        return self.categories
    
    def get_headers_by_category(self, category_name):
        return self.header_by_category.get(category_name, [])
    
    def get_content_by_header(self, header_name):
        return self.content_by_header.get(header_name, [])
  
    