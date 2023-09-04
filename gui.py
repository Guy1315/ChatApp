import tkinter as tk
from tkinter import scrolledtext, Button

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.text_area = tk.scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.input_area = tk.Text(root, height=3)
        self.input_area.pack(padx=20, pady=5, expand = False)

        self.send_button = Button(root, text="Send")
        self.send_button.pack()
