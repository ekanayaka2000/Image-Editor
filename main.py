import tkinter as tk
from tkinter import ttk
from ui import setup_ui

def main():
    # Initialize the main application window
    root = tk.Tk()
    root.geometry("1050x600")
    root.title("Image Editor")
    root.config(bg="#2e2e2e")

    # Setup UI
    canvas, bottom_frame, sliders, labels, buttons = setup_ui(root)

    root.mainloop()

if __name__ == "__main__":
    main()
