import customtkinter as ctk

class FileDropdown(ctk.CTkOptionMenu):
    
    def __init__(self, parent, command):
        
        self.parent_command = command
        self.file_list = []  # Initialize an empty list for file names
        self.path_map = {}  # Initialize an empty dictionary for path mapping
        
        
        super().__init__(parent, values=self.file_list, command=self.on_file_selected)
        
        self.set("Select a file")
        
    def update_file_list(self, files):
        for file in files:
            self.file_list.append(str(file.name).removesuffix(".txt"))  # Convert Path objects to strings
            self.path_map[str(file.name).removesuffix(".txt")] = file  # Map the string to the Path object
        self.configure(values=self.file_list)
        
    def on_file_selected(self, selected_file):
        if (self.path_map[selected_file]):
            self.parent_command(self.path_map[selected_file])