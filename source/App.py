import tkinter as tk
from source.view.view import View
from source.model.model import Model
from source.controller.controller import Controller

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.model = Model()
        self.view = View(self)
        self.controller = Controller(self.model, self.view) 
        
        self.title("iNav Diff Picker")
        self.geometry("800x600")