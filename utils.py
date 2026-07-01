import cv2
import numpy as np


def uploaded_file_to_rgb_image(uploaded_file):
    """
    Convert a Streamlit uploaded file into an RGB image.

    Streamlit gives us file bytes.
    OpenCV decodes those bytes into an image.
    OpenCV uses BGR color order, so we convert BGR to RGB.
    """

    file_bytes = uploaded_file.read()

    # Convert bytes into a NumPy array
    np_array = np.frombuffer(file_bytes, np.uint8)

    # Decode image from memory
    bgr_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if bgr_image is None:
        raise ValueError("Could not read the uploaded image.")

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    return rgb_image