import cv2


def load_chart(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not load the image.")

    return image


def get_image_info(image):
    height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels
    }


def resize_image(image, max_width=1500):
    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(image, (new_width, new_height))

    return resized


# Testing
if __name__ == "__main__":
    image = load_chart("test_chart.png")

    print("Image loaded successfully!")

    info = get_image_info(image)
    print("Original image information:", info)

    resized_image = resize_image(image)

    success = cv2.imwrite("processed_chart.png", resized_image)
    print("Processed image saved:", success)

    resized_info = get_image_info(resized_image)
    print("Resized image information:", resized_info)

import pandas as pd
import numpy as np
from color_analyzer import get_dominant_colors

def extract_chart_data_from_image(image_array, num_categories=4):
    """
    Scans the uploaded image pixels, clusters them into primary chart segments,
    and returns a structured DataFrame ready for dev3.py shape/pattern rendering.
    """
    # 1. Get dominant color clusters
    colors = get_dominant_colors(image_array, num_colors=num_categories)
    
    # 2. Count approximate pixel area for each color cluster (chart segments)
    pixels = np.array(image_array).reshape(-1, 3)
    counts = []
    labels = []
    
    for idx, col in enumerate(colors):
        # Calculate pixel distance to cluster center
        dist = np.linalg.norm(pixels - np.array(col), axis=1)
        count = int(np.sum(dist < 50))  # Match pixels within color threshold
        counts.append(max(count, 10))   # Safety minimum
        labels.append(f"Segment {idx + 1}")

    # 3. Output clean dataframe with categories and values
    return pd.DataFrame({
        "Chart Segment": labels,
        "Relative Size": counts
    })
