import customtkinter as ctk
import math

from source.view.file_view.file_subblock import FileSubBlock

class FileReader(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.categories = []
        self.category_views = {}
    
    def create_widgets(self):
        self.categories = self.parent.parent.controller.get_list_of_categories()
        self.category_selector = ctk.CTkSegmentedButton(self, values=self.categories, command=self.on_category_selected)
        self.category_selector.pack(padx=10, pady=10, fill="x")
        
    def on_category_selected(self, selected_category):
        if selected_category in self.category_views:
            self.category_views[selected_category].tkraise()
        else:
            content = self.parent.controller.get_category_content(selected_category)
            subblock = FileSubBlock(self)
            subblock.set_category(selected_category)
            
            label = ctk.CTkLabel(subblock.content_frame, text=content[0] if content else "", anchor="center", justify="center", wraplength=400)
            subblock.add_content(label)
            
            self.category_views[selected_category] = subblock
            subblock.pack(padx=10, pady=10, fill="both", expand=True)
        
    
