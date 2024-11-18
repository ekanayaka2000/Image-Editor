# Image Editor Application

This is a simple image editor application built using Python and the Tkinter library. The application allows users to perform various image editing operations such as rotating, cropping, adjusting brightness and contrast, applying filters, and more.

## Features

- Load Image: Load an image from the file system.
- Rotate Image: Rotate the image left or right by 90 degrees.
- Crop Image: Crop a selected area of the image.
- Adjust Brightness: Increase or decrease the brightness of the image.
- Adjust Contrast: Increase or decrease the contrast of the image.
- Adjust Saturation: Change the saturation level of the image.
- Apply Filters: Apply various filters like edge detection, emboss, blur, and sharpen.
- Face Detection: Detect faces in the image.
- Save Image: Save the edited image to the file system.

## Requirements

- Python 3.x
- Tkinter
- Pillow
- OpenCV (for face detection)

## Run the main application

Use the UI to load an image and perform various editing operations.

## File Structure

- `main.py`: Entry point of the application. Initializes the main window and sets up the UI.
- `ui.py`: Contains functions to set up the user interface and handle UI events.
- `handlers.py`: Contains functions to handle various image editing operations.
- `rotate_controls.py`: Contains functions related to rotating the image.

## Functions

### `main.py`

- `main()`: Initializes the main application window and sets up the UI.

### `ui.py`

- `setup_ui(root)`: Sets up the user interface components.
- `rotate_left(canvas, rotate_slider, rotate_value_label)`: Rotates the image 90 degrees to the left.
- `rotate_right(canvas, rotate_slider, rotate_value_label)`: Rotates the image 90 degrees to the right.

### `handlers.py`

- `add_image(canvas)`: Opens a file dialog to select an image and loads it onto the canvas.
- `auto_invert(canvas)`: Automatically inverts the colors of the image.
- `add_censorship(canvas)`: Adds censorship to the image.
- `crop_image(canvas)`: Crops the selected area of the image.
- `start_crop(event, canvas)`: Starts the cropping process.
- `draw_crop_rect(event, canvas)`: Draws the cropping rectangle.
- `finish_crop(event, canvas)`: Finishes the cropping process.
- `undo_crop(canvas)`: Undoes the last crop operation.
- `show_saturation_controls(canvas, bottom_frame, sliders)`: Shows the saturation controls.
- `change_saturation(canvas, saturation_value)`: Changes the saturation of the image.
- `update_saturation_value(canvas, saturation_slider, saturation_value_label)`: Updates the saturation value.
- `reset_saturation(canvas, saturation_slider, saturation_value_label)`: Resets the saturation to the default value.
- `apply_edge_detection(canvas)`: Applies edge detection to the image.
- `detect_faces(canvas)`: Detects faces in the image.
- `show_brightness_controls(canvas, bottom_frame, sliders)`: Shows the brightness controls.
- `change_brightness(canvas, brightness_value)`: Changes the brightness of the image.
- `update_brightness_value(canvas, brightness_slider, brightness_value_label)`: Updates the brightness value.
- `reset_brightness(canvas, brightness_slider, brightness_value_label)`: Resets the brightness to the default value.
- `show_contrast_controls(canvas, bottom_frame, sliders)`: Shows the contrast controls.
- `change_contrast(canvas, contrast_value)`: Changes the contrast of the image.
- `update_contrast_value(canvas, contrast_slider, contrast_value_label)`: Updates the contrast value.
- `reset_contrast(canvas, contrast_slider, contrast_value_label)`: Resets the contrast to the default value.
- `apply_emboss(canvas)`: Applies emboss filter to the image.
- `apply_blur_sharpen(canvas, value)`: Applies blur or sharpen filter to the image.
- `show_blur_sharpen_controls(canvas, bottom_frame, sliders)`: Shows the blur/sharpen controls.
- `update_blur_sharpen_value(canvas, blur_sharpen_slider, blur_sharpen_value_label)`: Updates the blur/sharpen value.
- `reset_blur_sharpen(canvas, blur_sharpen_slider, blur_sharpen_value_label)`: Resets the blur/sharpen to the default value.
- `save_current_edit(canvas)`: Saves the current edit.
- `save_image(canvas)`: Saves the image to the file system.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Pillow
- OpenCV
- Tkinter
 
