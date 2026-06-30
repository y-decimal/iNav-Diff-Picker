class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)  # Set the controller in the view
        
    def get_file_list(self):
        # Logic to get the list of files from the model
        return self.model.get_files()