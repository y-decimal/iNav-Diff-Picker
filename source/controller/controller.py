# Temporary fixed file paths for testing purposes

source_directory = "source/model/source_diffs"
output_directory = "source/model/output_diffs"

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)  # Set the controller in the view
        
    def get_file_list(self):
        # Logic to get the list of files from the model
        return self.model.get_files(source_directory)
    
    def set_active_file(self, file_name):
        # Logic to set the active file in the model
        self.model.set_active_file(file_name)
        
    def get_active_file_content(self):
        # Logic to get the content of the active file from the model
        return self.model.get_active_file_content()
    
    def get_list_of_categories(self):
        # Logic to get the list of categories from the model
        return self.model.get_list_of_categories()