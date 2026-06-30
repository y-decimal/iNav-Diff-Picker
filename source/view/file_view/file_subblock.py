import customtkinter as ctk

class FileSubBlock(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.header_name = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"))
        self.header_name.pack(padx=10, pady=10, fill="x")
        
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
    def set_header(self, header_name):
        self.header_name.configure(text=header_name)
    
    def add_content(self, content_list):
        for content_string in content_list:
            for block in content_string:
                if block.startswith("#"):
                    continue
                content_widget = ctk.CTkLabel(self.content_frame, text=block, anchor="center", justify="left", wraplength=400, font=("Arial", 18))
                content_widget.pack(padx=5, pady=5, fill="both", expand=True)