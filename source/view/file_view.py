import tkinter as tk
import customtkinter as ctk

class FileView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Create a label
        self.label = ctk.CTkLabel(self, text="File View")
        self.label.pack(pady=20)

        # Create a button
        self.button = ctk.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        self.label.configure(text="Button Clicked!")