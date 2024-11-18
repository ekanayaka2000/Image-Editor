from PIL import ImageEnhance, ImageTk, Image

def change_brightness(canvas, brightness_value):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        enhancer = ImageEnhance.Brightness(pil_image)
        factor = brightness_value / 50  # Default value is 50, so we scale accordingly
        enhanced_image = enhancer.enhance(factor)
        
        # Resize image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        enhanced_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(enhanced_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")

def change_contrast(canvas, contrast_value):
    if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        enhancer = ImageEnhance.Contrast(pil_image)
        factor = contrast_value / 50  # Default value is 50, so we scale accordingly
        enhanced_image = enhancer.enhance(factor)
        
        # Resize image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        enhanced_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        canvas.image = ImageTk.PhotoImage(enhanced_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
