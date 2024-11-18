from random import randint
from tkinter import filedialog, ttk
from PIL import Image, ImageTk,ImageOps,ImageFilter,ImageEnhance
from PIL import ImageFilter
import cv2
import numpy as np
from image_operations import (
    change_brightness, change_contrast
)

def add_image(canvas):
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if not file_path:
        return

    # Load the image using PIL
    pil_image = Image.open(file_path)
    
    # Store the original image to reset modifications
    canvas.original_image = pil_image.copy()
    
    # Resize image to fit into canvas while maintaining aspect ratio
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
    
    canvas.image = ImageTk.PhotoImage(pil_image)

    # Clear the canvas and add the image
    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")

def auto_invert(canvas):
    # Auto invert the image
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        inverted_image = ImageOps.invert(pil_image)

        # Resize inverted image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        inverted_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

        canvas.image = ImageTk.PhotoImage(inverted_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image  # Maintain reference to avoid garbage collection
        canvas.update_idletasks()  # Force canvas update

def add_censorship(canvas):
    if hasattr(canvas, 'image'):
        pil_image = canvas.original_image.copy()
        pil_image = pil_image.convert("RGB")
        
        # Convert PIL image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Load the pre-trained Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces in the image
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Apply blur to each face region
        for (x, y, w, h) in faces:
            face = open_cv_image[y:y+h, x:x+w]
            face = cv2.GaussianBlur(face, (99, 99), 30)  # Adjust kernel size for more or less blur
            open_cv_image[y:y+h, x:x+w] = face
        
        # Convert OpenCV image back to PIL format
        pil_image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
        
        # Resize the blurred image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

        canvas.image = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image
        canvas.update_idletasks()

def crop_image(canvas):
    if hasattr(canvas, 'original_image'):
        # Set cursor to plus sign
        canvas.config(cursor="plus")

        # Bind mouse events for cropping
        canvas.bind("<ButtonPress-1>", lambda event: start_crop(event, canvas))
        canvas.bind("<B1-Motion>", lambda event: draw_crop_rect(event, canvas))
        canvas.bind("<ButtonRelease-1>", lambda event: finish_crop(event, canvas))

def start_crop(event, canvas):
    canvas.crop_start_x = event.x
    canvas.crop_start_y = event.y
    canvas.crop_rect = canvas.create_rectangle(canvas.crop_start_x, canvas.crop_start_y, event.x, event.y, outline='red')

def draw_crop_rect(event, canvas):
    canvas.coords(canvas.crop_rect, canvas.crop_start_x, canvas.crop_start_y, event.x, event.y)

def finish_crop(event, canvas):
    canvas.crop_end_x = event.x
    canvas.crop_end_y = event.y
    canvas.delete(canvas.crop_rect)

    # Restore the cursor to default
    canvas.config(cursor="")

    if hasattr(canvas, 'original_image'):
        if not hasattr(canvas, 'crop_history'):
            canvas.crop_history = []
        canvas.crop_history.append(canvas.original_image.copy())

        pil_image = canvas.original_image.copy()
        width, height = pil_image.size
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        crop_box = (
            int(canvas.crop_start_x * width / canvas_width),
            int(canvas.crop_start_y * height / canvas_height),
            int(canvas.crop_end_x * width / canvas_width),
            int(canvas.crop_end_y * height / canvas_height)
        )

        cropped_image = pil_image.crop(crop_box)

        canvas.original_image = cropped_image
        canvas.image = ImageTk.PhotoImage(cropped_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        
def undo_crop(canvas):
    if hasattr(canvas, 'crop_history') and canvas.crop_history:
        canvas.original_image = canvas.crop_history.pop()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        pil_image = canvas.original_image.copy()
        pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

        canvas.image = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")

        # Hide the Undo Crop button
        canvas.undo_crop_button.pack_forget()


def show_saturation_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    saturation_slider, saturation_value_label, reset_saturation_button, save_saturation_button = sliders["saturation"]
    saturation_slider.pack(side="left", padx=20)
    saturation_value_label.pack(side="left", padx=10)
    reset_saturation_button.pack(side="left", padx=10)
    save_saturation_button.pack(side="left", padx=10)
    saturation_slider.set(50)
    saturation_value_label.config(text="50")
    change_saturation(canvas, 50)
    saturation_slider.bind("<Motion>", lambda event: update_saturation_value(canvas, saturation_slider, saturation_value_label))


def change_saturation(canvas, saturation_value):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        
        # Enhance the saturation
        enhancer = ImageEnhance.Color(pil_image)
        pil_image = enhancer.enhance(saturation_value / 50.0)  # Scale 0-100 slider to 0-2 for enhancement
        
        # Resize the image to fit into the canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image  # Maintain reference to avoid garbage collection
        canvas.update_idletasks()  # Force canvas update

def update_saturation_value(canvas, saturation_slider, saturation_value_label):
    saturation_value = saturation_slider.get()
    saturation_value_label.config(text=str(int(saturation_value)))
    change_saturation(canvas, saturation_value)

def reset_saturation(canvas, saturation_slider, saturation_value_label):
    saturation_slider.set(50)
    saturation_value_label.config(text="50")
    change_saturation(canvas, 50)


def apply_edge_detection(canvas):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        
        # Convert PIL image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Apply edge detection using Canny
        edges = cv2.Canny(open_cv_image, 100, 200)
        
        # Convert edges to 3-channel image
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # Convert OpenCV image back to PIL format
        pil_image_with_edges = Image.fromarray(edges)
        
        # Resize the edge-detected image to fit into the canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        pil_image_with_edges.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(pil_image_with_edges)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image
        canvas.update_idletasks()


def detect_faces(canvas):
    print("Detecting faces...")
    if not hasattr(canvas, 'original_image'):
        return

    pil_image = canvas.original_image.convert('RGB')
    open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        return

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(open_cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    pil_image_with_faces = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    pil_image_with_faces.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

    canvas.image = ImageTk.PhotoImage(pil_image_with_faces)
    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
    canvas.image_reference = canvas.image
    canvas.update_idletasks()


def show_brightness_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    brightness_slider, brightness_value_label, reset_brightness_button, save_brightness_button = sliders["brightness"]
    brightness_slider.pack(side="left", padx=20)
    brightness_value_label.pack(side="left", padx=10)
    reset_brightness_button.pack(side="left", padx=10)
    save_brightness_button.pack(side="left", padx=10)
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)
    brightness_slider.bind("<Motion>", lambda event: update_brightness_value(canvas, brightness_slider, brightness_value_label))

def show_contrast_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    contrast_slider, contrast_value_label, reset_contrast_button, save_contrast_button = sliders["contrast"]
    contrast_slider.pack(side="left", padx=20)
    contrast_value_label.pack(side="left", padx=10)
    reset_contrast_button.pack(side="left", padx=10)
    save_contrast_button.pack(side="left", padx=10)
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)
    contrast_slider.bind("<Motion>", lambda event: update_contrast_value(canvas, contrast_slider, contrast_value_label))

def update_brightness_value(canvas, brightness_slider, brightness_value_label):
    brightness_value = brightness_slider.get()
    brightness_value_label.config(text=str(int(brightness_value)))
    change_brightness(canvas, brightness_value)

def update_contrast_value(canvas, contrast_slider, contrast_value_label):
    contrast_value = contrast_slider.get()
    contrast_value_label.config(text=str(int(contrast_value)))
    change_contrast(canvas, contrast_value)


def reset_brightness(canvas, brightness_slider, brightness_value_label):
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)

def reset_contrast(canvas, contrast_slider, contrast_value_label):
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)

def save_current_edit(canvas):
    if hasattr(canvas, 'image'):
        canvas.current_image = ImageTk.getimage(canvas.image)    




def show_brightness_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    brightness_slider, brightness_value_label, reset_brightness_button, save_brightness_button = sliders["brightness"]
    brightness_slider.pack(side="left", padx=20)
    brightness_value_label.pack(side="left", padx=10)
    reset_brightness_button.pack(side="left", padx=10)
    save_brightness_button.pack(side="left", padx=10)
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)
    brightness_slider.bind("<Motion>", lambda event: update_brightness_value(canvas, brightness_slider, brightness_value_label))

def show_contrast_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    contrast_slider, contrast_value_label, reset_contrast_button, save_contrast_button = sliders["contrast"]
    contrast_slider.pack(side="left", padx=20)
    contrast_value_label.pack(side="left", padx=10)
    reset_contrast_button.pack(side="left", padx=10)
    save_contrast_button.pack(side="left", padx=10)
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)
    contrast_slider.bind("<Motion>", lambda event: update_contrast_value(canvas, contrast_slider, contrast_value_label))

def update_brightness_value(canvas, brightness_slider, brightness_value_label):
    brightness_value = brightness_slider.get()
    brightness_value_label.config(text=str(int(brightness_value)))
    change_brightness(canvas, brightness_value)

def update_contrast_value(canvas, contrast_slider, contrast_value_label):
    contrast_value = contrast_slider.get()
    contrast_value_label.config(text=str(int(contrast_value)))
    change_contrast(canvas, contrast_value)


def reset_brightness(canvas, brightness_slider, brightness_value_label):
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)

def reset_contrast(canvas, contrast_slider, contrast_value_label):
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)
    
def apply_emboss(canvas):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        
        # Apply emboss filter
        embossed_image = pil_image.filter(ImageFilter.EMBOSS)
        
        # Resize the embossed image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        embossed_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

        canvas.image = ImageTk.PhotoImage(embossed_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image
        canvas.update_idletasks()
        
def apply_blur_sharpen(canvas, value):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        
        if value < 50:
            factor = (50 - value) / 10.0  # Sharpen factor
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1 + factor)
        elif value > 50:
            factor = (value - 50) / 50.0  # Blur factor
            pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=factor * 5))

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image
        canvas.update_idletasks()

def show_blur_sharpen_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    blur_sharpen_slider, blur_sharpen_value_label, reset_blur_sharpen_button, save_blur_sharpen_button = sliders["blur_sharpen"]
    blur_sharpen_slider.pack(side="left", padx=20)
    blur_sharpen_value_label.pack(side="left", padx=10)
    reset_blur_sharpen_button.pack(side="left", padx=10)
    save_blur_sharpen_button.pack(side="left", padx=10)
    blur_sharpen_slider.set(50)
    blur_sharpen_value_label.config(text="50")
    apply_blur_sharpen(canvas, 50)
    blur_sharpen_slider.bind("<Motion>", lambda event: update_blur_sharpen_value(canvas, blur_sharpen_slider, blur_sharpen_value_label))

def update_blur_sharpen_value(canvas, blur_sharpen_slider, blur_sharpen_value_label):
    blur_sharpen_value = blur_sharpen_slider.get()
    blur_sharpen_value_label.config(text=str(int(blur_sharpen_value)))
    apply_blur_sharpen(canvas, blur_sharpen_value)

def reset_blur_sharpen(canvas, blur_sharpen_slider, blur_sharpen_value_label):
    blur_sharpen_slider.set(50)
    blur_sharpen_value_label.config(text="50")
    apply_blur_sharpen(canvas, 50)


def save_current_edit(canvas):
    if hasattr(canvas, 'image'):
        canvas.current_image = ImageTk.getimage(canvas.image)    

def save_image(canvas):
    if hasattr(canvas, 'image'):
        # Get the current image from the canvas
        current_image = ImageTk.getimage(canvas.image)
        
        # Open a file dialog to choose where to save the image
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            # Save the image to the chosen file path
            current_image.save(file_path)
            print(f"Image saved to {file_path}")
    else:
        print("No image to save")
