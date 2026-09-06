import cv2
import numpy as np
from chart_processor import load_chart, resize_image


def simulate_protanopia(image):
    # Convert OpenCV's BGR format to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Normalize pixel values from 0-255 to 0-1
    rgb = rgb / 255.0

    # Protanopia transformation matrix
    matrix = np.array([
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758]
    ])

    # Apply the transformation
    simulated = np.dot(rgb, matrix.T)

    # Keep values between 0 and 1
    simulated = np.clip(simulated, 0, 1)

    # Convert back to 0-255 image format
    simulated = (simulated * 255).astype(np.uint8)

    # Convert RGB back to OpenCV's BGR format
    simulated = cv2.cvtColor(simulated, cv2.COLOR_RGB2BGR)

    return simulated


def simulate_deuteranopia(image):
    # Convert OpenCV's BGR format to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Normalize pixel values from 0-255 to 0-1
    rgb = rgb / 255.0

    # Deuteranopia transformation matrix
    matrix = np.array([
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700]
    ])

    # Apply the transformation
    simulated = np.dot(rgb, matrix.T)

    # Keep values between 0 and 1
    simulated = np.clip(simulated, 0, 1)

    # Convert back to 0-255 image format
    simulated = (simulated * 255).astype(np.uint8)

    # Convert RGB back to OpenCV's BGR format
    simulated = cv2.cvtColor(simulated, cv2.COLOR_RGB2BGR)

    return simulated


def simulate_tritanopia(image):
    # Convert OpenCV's BGR format to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Normalize pixel values from 0-255 to 0-1
    rgb = rgb / 255.0

    # Tritanopia transformation matrix
    matrix = np.array([
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525]
    ])

    # Apply the transformation
    simulated = np.dot(rgb, matrix.T)

    # Keep values between 0 and 1
    simulated = np.clip(simulated, 0, 1)

    # Convert back to 0-255 image format
    simulated = (simulated * 255).astype(np.uint8)

    # Convert RGB back to OpenCV's BGR format
    simulated = cv2.cvtColor(simulated, cv2.COLOR_RGB2BGR)

    return simulated


# Load the original chart
image = load_chart("test_chart.png")

# Resize the chart for processing
image = resize_image(image)

# Simulate Protanopia
protanopia_image = simulate_protanopia(image)
cv2.imwrite("protanopia_chart.png", protanopia_image)

# Simulate Deuteranopia
deuteranopia_image = simulate_deuteranopia(image)
cv2.imwrite("deuteranopia_chart.png", deuteranopia_image)

# Simulate Tritanopia
tritanopia_image = simulate_tritanopia(image)
cv2.imwrite("tritanopia_chart.png", tritanopia_image)

print("CVD simulations complete!")
