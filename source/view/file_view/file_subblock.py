import customtkinter as ctk

class FileSubBlock(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.category_header = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"))
        self.category_header.pack(padx=10, pady=10, fill="x")
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
    def set_category(self, category_name):
        self.category_header.configure(text=category_name)
    
    def add_content(self, content_widget):
        content_widget.pack(in_=self.content_frame, padx=5, pady=5, fill="both", expand=True)