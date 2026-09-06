import cv2
import numpy as np


def get_dominant_colors(image, k=5):
    """
    Find the most common colors in an image.
    Returns colors as RGB tuples.
    """

    image = np.array(image)

    # Convert image to a simple list of pixels
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    # K-means criteria
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        100,
        0.2
    )

    # Find dominant colors
    _, labels, centers = cv2.kmeans(
        pixels,
        k,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    centers = np.uint8(centers)

    # Count how often each color appears
    counts = np.bincount(labels.flatten())

    # Sort colors by frequency
    sorted_indices = np.argsort(counts)[::-1]

    dominant_colors = []

    for index in sorted_indices:
        color = tuple(centers[index])
        dominant_colors.append(color)

    return dominant_colors


def color_distance(color1, color2):
    """
    Calculate the distance between two RGB colors.
    Smaller distance = more similar colors.
    """

    color1 = np.array(color1, dtype=float)
    color2 = np.array(color2, dtype=float)

    return np.linalg.norm(color1 - color2)


def calculate_brightness(color):
    """
    Calculate approximate brightness of an RGB color.
    """

    r, g, b = color

    return (
        0.299 * r +
        0.587 * g +
        0.114 * b
    )


def analyze_colors(image):
    """
    Analyze an uploaded visualization for
    potentially problematic colors.
    """

    colors = get_dominant_colors(image)

    issues = []

    # Check for colors that are too similar
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):

            distance = color_distance(
                colors[i],
                colors[j]
            )

            if distance < 60:
                issues.append({
                    "type": "Similar Colors",
                    "message": (
                        f"Colors {colors[i]} and {colors[j]} "
                        "may be difficult to distinguish."
                    ),
                    "severity": "High"
                })

    # Check for potentially low contrast
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):

            brightness1 = calculate_brightness(colors[i])
            brightness2 = calculate_brightness(colors[j])

            brightness_difference = abs(
                brightness1 - brightness2
            )

            if brightness_difference < 40:
                issues.append({
                    "type": "Low Contrast",
                    "message": (
                        f"Colors {colors[i]} and {colors[j]} "
                        "have low brightness contrast."
                    ),
                    "severity": "Medium"
                })

    # Remove duplicate issues
    unique_issues = []

    seen = set()

    for issue in issues:

        key = (
            issue["type"],
            issue["message"]
        )

        if key not in seen:
            unique_issues.append(issue)
            seen.add(key)

    return {
        "colors": colors,
        "issues": unique_issues,
        "issue_count": len(unique_issues)
    }
