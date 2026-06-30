import customtkinter as ctk
import math

from source.view.file_view.file_subblock import FileSubBlock

class FileReader(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.categories = []
        
        self.subblocks = []
    
    def create_widgets(self):
        self.categories = self.parent.parent.controller.get_list_of_categories()
        self.category_selector = ctk.CTkSegmentedButton(self, values=self.categories, command=self.on_category_selected)
        self.category_selector.pack(padx=10, pady=10, fill="x")
        
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        
    def on_category_selected(self, selected_category):
        print("Category selected: ", str(selected_category))
        headers = self.parent.parent.controller.get_headers_by_category(selected_category)
        self.display_headers(headers)
        
        
    def display_headers(self, headers):
        # Clear existing subblocks if any
        for subblock in self.subblocks:
            subblock.destroy()
        self.subblocks = []
        
        for header in headers:
            if isinstance(header, list):
                header = header[0] if header else ""
            if not header:
                continue
            content = self.parent.parent.controller.get_content_by_header(header)
            if not content or content == "":
                continue
            
            subblock = FileSubBlock(self.frame)
            subblock.set_header(header)

            subblock.add_content(content)
            
            self.subblocks.append(subblock)
            
        cols = (len(self.subblocks) * (16 / 9)) / 2
        rows = math.ceil(len(self.subblocks) / cols)
        
        for subblock in self.subblocks:
            subblock.grid(column=self.subblocks.index(subblock) // rows, row=self.subblocks.index(subblock) % rows, padx=10, pady=10, sticky="nsew")
            
    
