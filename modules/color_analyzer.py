"""
color_analyzer.py
Developer 2 - Analytics Engineer (Percepta)

Responsibilities:
    1. Extract the top N dominant colors from an image's pixel array using
       K-Means clustering.
    2. Calculate the Euclidean (straight-line) distance between two colors
       in RGB space.
    3. Calculate the perceived brightness of a single color.

Input contract (from Developer 1):
    A NumPy array representing the image, shape (height, width, 3),
    dtype uint8, channel order RGB (make sure Developer 1 confirms this;
    OpenCV loads as BGR by default, so convert if needed).

Output contract (to accessibility.py / Developer 2's own Task 2):
    - get_dominant_colors() -> list of (R, G, B) tuples, ints 0-255
    - color_distance()      -> float
    - perceptual_brightness() -> float, 0-255 range
"""

import numpy as np
import cv2


def get_dominant_colors(image_array: np.ndarray, num_colors: int = 5) -> list:
    """
    Find the top `num_colors` most frequently used colors in an image
    using K-Means clustering.

    Args:
        image_array: np.ndarray of shape (H, W, 3), RGB, uint8.
        num_colors: how many dominant colors to extract (default 5).

    Returns:
        List of (R, G, B) int tuples, ordered by cluster size
        (most dominant first).
    """
    if image_array is None or image_array.size == 0:
        raise ValueError("image_array is empty or None")

    # Flatten the image to a list of pixels: (H*W, 3)
    pixels = image_array.reshape(-1, 3).astype(np.float32)

    # K-Means needs criteria: (type, max_iter, epsilon)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.2)

    # attempts = how many times K-Means reruns with different seeds,
    # keeping the best result (lowest compactness)
    _compactness, labels, centers = cv2.kmeans(
        pixels,
        num_colors,
        None,
        criteria,
        attempts=10,
        flags=cv2.KMEANS_RANDOM_CENTERS,
    )

    # Count how many pixels fall into each cluster so we can rank them
    labels = labels.flatten()
    counts = np.bincount(labels, minlength=num_colors)

    # Sort cluster indices by size, descending (most dominant first)
    order = np.argsort(-counts)

    dominant_colors = []
    for idx in order:
        r, g, b = centers[idx]
        dominant_colors.append((int(round(r)), int(round(g)), int(round(b))))

    return dominant_colors


def color_distance(color_a: tuple, color_b: tuple) -> float:
    """
    Euclidean distance between two RGB colors.

    Args:
        color_a: (R, G, B) tuple
        color_b: (R, G, B) tuple

    Returns:
        float distance. 0 = identical colors.
        Max possible distance in RGB space is ~441.7 (black to white).
    """
    a = np.array(color_a, dtype=np.float64)
    b = np.array(color_b, dtype=np.float64)
    return float(np.linalg.norm(a - b))


def perceptual_brightness(color: tuple) -> float:
    """
    Calculate the perceived brightness of a color using the standard
    luminance-weighting formula (human eyes are more sensitive to green,
    less to blue).

    Formula: 0.299*R + 0.587*G + 0.114*B

    Args:
        color: (R, G, B) tuple

    Returns:
        float brightness value, 0 (black) to 255 (white).
    """
    r, g, b = color
    return float(0.299 * r + 0.587 * g + 0.114 * b)


if __name__ == "__main__":
    # Quick manual smoke test - run this file directly to sanity check.
    # Creates a fake 100x100 image split into 3 solid color blocks.
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    test_img[:, :33] = [255, 0, 0]     # red block
    test_img[:, 33:66] = [0, 255, 0]   # green block
    test_img[:, 66:] = [0, 0, 255]     # blue block

    colors = get_dominant_colors(test_img, num_colors=3)
    print("Dominant colors found:", colors)

    if len(colors) >= 2:
        dist = color_distance(colors[0], colors[1])
        print(f"Distance between color 0 and 1: {dist:.2f}")

    for c in colors:
        print(f"Brightness of {c}: {perceptual_brightness(c):.2f}")
