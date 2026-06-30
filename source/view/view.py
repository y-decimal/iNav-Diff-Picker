import tkinter as tk
from tkinter import ttk

from source.view.theme import apply_theme

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        apply_theme(self)
        
        self.create_widgets()

    def create_widgets(self):
        # Create a label
        self.label = ttk.Label(self, text="Welcome to iNav Diff Picker!")
        self.label.pack(pady=20)

        # Create a button
        self.button = ttk.Button(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        self.label.config(text="Button Clicked!")