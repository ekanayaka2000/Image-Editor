import tkinter as tk
from tkinter import ttk
from handlers import (
    add_image, auto_invert, add_censorship, crop_image, undo_crop, save_current_edit,save_image,
    show_brightness_controls, show_contrast_controls, change_saturation, reset_saturation, show_saturation_controls, apply_edge_detection, apply_emboss, reset_blur_sharpen, show_blur_sharpen_controls, update_blur_sharpen_value, detect_faces, reset_brightness, reset_contrast
)
from rotate_controls import change_rotate, rotate_image, update_rotate_value, reset_rotate, save_current_edit

def rotate_left(canvas, rotate_slider, rotate_value_label):
    """Rotate the image 90 degrees to the left."""
    current_value = rotate_slider.get()
    new_value = (current_value - 90) % 360
    rotate_slider.set(new_value)
    update_rotate_value(canvas, rotate_slider, rotate_value_label)

def rotate_right(canvas, rotate_slider, rotate_value_label):
    """Rotate the image 90 degrees to the right."""
    current_value = rotate_slider.get()
    new_value = (current_value + 90) % 360
    rotate_slider.set(new_value)
    update_rotate_value(canvas, rotate_slider, rotate_value_label)

def setup_ui(root):
    # Create the main frame to hold the left and canvas frames
    main_frame = ttk.Frame(root)
    main_frame.pack(side="top", fill="both", expand=True)

    # Create the left frame
    left_frame = ttk.Frame(main_frame, width=350)
    left_frame.pack(side="left", fill="y")
    left_frame.config(style="TFrame")

    # Create the canvas frame (right side)
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.pack(side="right", fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#3c3f41")
    canvas.pack(fill="both", expand=True)

    # Create the bottom frame for the sliders (but don't pack it initially)
    bottom_frame = ttk.Frame(root, height=50)
    bottom_frame.config(style="TFrame")

    # Brightness slider, label, and reset button
    brightness_slider = ttk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=700)
    brightness_value_label = ttk.Label(bottom_frame, text="50", style="TLabel")
    reset_brightness_button = ttk.Button(bottom_frame, text="Reset Brightness",
                                         command=lambda: reset_brightness(canvas, brightness_slider, brightness_value_label))
    save_brightness_button = ttk.Button(bottom_frame, text="✓", width=3,
                                        command=lambda: save_current_edit(canvas))

    # Contrast slider, label, and reset button
    contrast_slider = ttk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=700)
    contrast_value_label = ttk.Label(bottom_frame, text="50", style="TLabel")
    reset_contrast_button = ttk.Button(bottom_frame, text="Reset Contrast",
                                       command=lambda: reset_contrast(canvas, contrast_slider, contrast_value_label))
    save_contrast_button = ttk.Button(bottom_frame, text="✓", width=3,
                                      command=lambda: save_current_edit(canvas))

    # Rotate controls
    rotate_slider = ttk.Scale(bottom_frame, from_=0, to=360, orient=tk.HORIZONTAL, length=700)
    rotate_value_label = ttk.Label(bottom_frame, text="0", style="TLabel")
    reset_rotate_button = ttk.Button(bottom_frame, text="Reset Rotate",
                                     command=lambda: reset_rotate(canvas, rotate_slider, rotate_value_label))
    save_rotate_button = ttk.Button(bottom_frame, text="✓", width=3,
                                    command=lambda: save_current_edit(canvas))

    # Add left and right rotate buttons
    rotate_left_button = ttk.Button(bottom_frame, text=" ← ", width=5,
                                    command=lambda: rotate_left(canvas, rotate_slider, rotate_value_label))
    rotate_right_button = ttk.Button(bottom_frame, text=" → ", width=5,
                                     command=lambda: rotate_right(canvas, rotate_slider, rotate_value_label))

    rotate_slider.config(command=lambda v: update_rotate_value(canvas, rotate_slider, rotate_value_label))

    # Create the undo crop button
    undo_crop_button = ttk.Button(bottom_frame, text="Undo Crop", command=lambda: undo_crop(canvas))
    undo_crop_button.pack(side="left", padx=10)
    undo_crop_button.pack_forget()  # Hide initially
    
    # Saturation slider, label, and reset button
    saturation_slider = ttk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=700)
    saturation_value_label = ttk.Label(bottom_frame, text="50", style="TLabel")
    reset_saturation_button = ttk.Button(bottom_frame, text="Reset Saturation",
                                         command=lambda: reset_saturation(canvas, saturation_slider, saturation_value_label))
    save_saturation_button = ttk.Button(bottom_frame, text="✓", width=3,
                                        command=lambda: save_current_edit(canvas))

    # Combined blur/sharpen slider and button
    blur_sharpen_slider = ttk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=700)
    blur_sharpen_value_label = ttk.Label(bottom_frame, text="50", style="TLabel")
    reset_blur_sharpen_button = ttk.Button(bottom_frame, text="Reset Blur/Sharpen",
                                           command=lambda: reset_blur_sharpen(canvas, blur_sharpen_slider, blur_sharpen_value_label))
    save_blur_sharpen_button = ttk.Button(bottom_frame, text="✓", width=3,
                                          command=lambda: save_current_edit(canvas))

    # Bind slider to update image
    blur_sharpen_slider.bind("<Motion>", lambda event: update_blur_sharpen_value(canvas, blur_sharpen_slider, blur_sharpen_value_label))

    # Pack combined blur/sharpen controls
    blur_sharpen_slider.pack(side="left", padx=20)
    blur_sharpen_value_label.pack(side="left", padx=10)
    reset_blur_sharpen_button.pack(side="left", padx=10)
    save_blur_sharpen_button.pack(side="left", padx=10)

    

    sliders = {
        "brightness": (brightness_slider, brightness_value_label, reset_brightness_button, save_brightness_button),
        "contrast": (contrast_slider, contrast_value_label, reset_contrast_button, save_contrast_button),
        "saturation": (saturation_slider, saturation_value_label, reset_saturation_button, save_saturation_button),
        "rotate": (rotate_slider, rotate_value_label, reset_rotate_button, save_rotate_button),
        "blur_sharpen": (blur_sharpen_slider, blur_sharpen_value_label, reset_blur_sharpen_button, save_blur_sharpen_button),
   }

    # Add buttons and bind them to the functions
    button_texts = [
        ("Open Image", lambda: add_image(canvas)),
        ("Auto Invert", lambda: auto_invert(canvas)),
        ("Add Censorship", lambda: add_censorship(canvas)),
        ("Rotate Image", lambda: rotate_image(canvas, bottom_frame, sliders)),
        ("Crop Image", lambda: crop_image(canvas)),
        ("Undo Crop", lambda: undo_crop(canvas)),
        ("Change Brightness", lambda: show_brightness_controls(canvas, bottom_frame, sliders)),
        ("Change Contrast", lambda: show_contrast_controls(canvas, bottom_frame, sliders)),
        ("Change Saturation", lambda: show_saturation_controls(canvas, bottom_frame, sliders)),
        ("Edge Detection", lambda: apply_edge_detection(canvas)),
        ("Emboss", lambda: apply_emboss(canvas)),
        ("Blur/Sharpen", lambda: show_blur_sharpen_controls(canvas, bottom_frame, sliders)),
        ("Face Detection", lambda: detect_faces(canvas)),
        ("Save Image", lambda: save_image(canvas))
    ]

    for text, command in button_texts:
        button = ttk.Button(left_frame, text=text, command=command, style="Custom.TButton")
        button.pack(pady=0.5, padx=5, fill='both')

    # Pack rotate controls
    rotate_left_button.pack(side="left", padx=(10, 5), pady=5)
    rotate_slider.pack(side="left", padx=(5, 5), pady=5, fill="x", expand=True)
    rotate_right_button.pack(side="left", padx=(5, 10), pady=5)
    rotate_value_label.pack(side="left", padx=(5, 5))
    reset_rotate_button.pack(side="left", padx=(5, 5))
    save_rotate_button.pack(side="left", padx=(5, 10))

    return canvas, bottom_frame, sliders, {
        "brightness": brightness_value_label,
        "saturation": saturation_value_label,
        "contrast": contrast_value_label,
        "blur_sharpen": blur_sharpen_value_label
    }, {
        "brightness": reset_brightness_button,
        "contrast": reset_contrast_button,
        "saturation": reset_saturation_button,
        "undo_crop": undo_crop_button,
        "blur_sharpen": reset_blur_sharpen_button
    }
