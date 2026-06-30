import customtkinter as ctk

class FileReader(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.category_header = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"))
        self.category_header.pack(padx=10, pady=10, fill="x")