import tkinter as tk
import customtkinter as ctk

from source.view.file_view import FileView

class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_view = FileView(self)
        self.controller = None  # Placeholder for the controller instance
    
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        
    def set_controller(self, controller):
        self.controller = controller
        
    def create_widgets(self):
        self.view_toggle = ctk.CTkSegmentedButton(self, values=["Files", "Editor"], font=("Arial", 14), command=self.toggle_view)
        self.view_toggle.pack(padx=10, pady=10, fill="x", anchor="n")
        self.view_toggle.set("Files")
        self.show_file_view()
        
    def show_file_view(self):
        self.file_view.pack(fill=tk.BOTH, expand=True)
    def hide_file_view(self):
        self.file_view.pack_forget()
        
    def toggle_view(self, selected_view: str):
                
        if selected_view == "Files":
            print("Files view selected")
            self.show_file_view()
            # Implement logic to switch to Files view
        elif selected_view == "Editor":
            print("Editor view selected")
            self.hide_file_view()
            # Implement logic to switch to Editor view