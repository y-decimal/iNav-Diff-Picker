import tkinter as tk
import customtkinter as ctk

from source.view.file_view.file_view import FileView

class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_view = FileView(self)
        self.controller = None  # Placeholder for the controller instance
    
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        
    def set_controller(self, controller):
        self.controller = controller
        self.file_view.on_initialized()  # Call on_initialized after setting the controller
        
    def create_widgets(self):
        self.show_file_view()
        
    def show_file_view(self):
        self.file_view.pack(fill=tk.BOTH, expand=True)
    def hide_file_view(self):
        self.file_view.pack_forget()
        