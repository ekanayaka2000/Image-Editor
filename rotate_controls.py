import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def change_rotate(canvas, rotate_value):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        
        # Rotate the image by the specified value
        rotated_image = pil_image.rotate(rotate_value, expand=True)
        
        # Resize image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        rotated_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(rotated_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")

def rotate_image(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for left_button, right_button, reset_button, save_button in sliders.values():
        left_button.pack_forget()
        right_button.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    
    left_rotate_button, right_rotate_button, reset_rotate_button, save_rotate_button = sliders["rotate"]
    left_rotate_button.pack(side="left", padx=20)
    right_rotate_button.pack(side="left", padx=10)
    reset_rotate_button.pack(side="left", padx=10)
    save_rotate_button.pack(side="left", padx=10)
    
    right_rotate_button.config(text="0")
    change_rotate(canvas, 0)  # Initialize with no rotation

def update_rotate_value(canvas, slider, label):
    rotate_value = slider.get()
    label.config(text=str(rotate_value))
    change_rotate(canvas, rotate_value)

def reset_rotate(canvas, slider, label):
    slider.set(0)  # Reset to 0 degrees
    label.config(text="0")
    change_rotate(canvas, 0)

def save_current_edit(canvas):
    # Implement saving the current edit
    pass
