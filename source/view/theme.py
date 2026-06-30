from tkinter import ttk


def apply_theme(root):
    style = ttk.Style(root)

    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    style.configure(".", font=("Arial", 11))
    style.configure("TFrame", background="#2c2c2c")
    style.configure("TLabel", background="#2c2c2c", foreground="#dbdbdb")
    style.configure(
        "TButton",
        padding=(14, 8),
        background="#2f5d62",
        foreground="#ffffff",
    )
    style.map(
        "TButton",
        background=[("active", "#3d777d"), ("pressed", "#24474b")],
        foreground=[("disabled", "#cfcfcf")],
    )
