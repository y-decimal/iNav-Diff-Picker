import tkinter as tk
import customtkinter as ctk

from source.view.file_view.file_dropdpwn import FileDropdown
from source.view.file_view.file_reader import FileReader

class FileView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        
        self.file_dropdown = FileDropdown(self, self.on_file_selected)
        self.file_dropdown.pack(padx=10, pady=10, fill="x")
        
        self.file_reader = FileReader(self)
        self.file_reader.pack(padx=10, pady=10, fill="both", expand=True)
       
    def on_initialized(self):
        if self.parent.controller:
            files = self.parent.controller.get_file_list()
            self.file_dropdown.update_file_list(files)
        else:
            print("Controller is not set.")
       
    def on_file_selected(self, selected_file):
        print("File selected: ", str(selected_file))