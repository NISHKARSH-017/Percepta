import cv2
import numpy as np


def simulate_cvd(image, cvd_type):
    """
    Simulate how an image may appear under different
    types of Color Vision Deficiency.

    cvd_type:
        - protanopia
        - deuteranopia
        - tritanopia
    """

    # Convert RGB image to a NumPy array
    image = np.array(image)

    # Convert RGB to BGR because OpenCV uses BGR
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # CVD transformation matrices
    matrices = {
        "protanopia": np.array([
            [0.567, 0.433, 0.000],
            [0.558, 0.442, 0.000],
            [0.000, 0.242, 0.758]
        ]),

        "deuteranopia": np.array([
            [0.625, 0.375, 0.000],
            [0.700, 0.300, 0.000],
            [0.000, 0.300, 0.700]
        ]),

        "tritanopia": np.array([
            [0.950, 0.050, 0.000],
            [0.000, 0.433, 0.567],
            [0.000, 0.475, 0.525]
        ])
    }

    if cvd_type not in matrices:
        raise ValueError(
            "CVD type must be protanopia, deuteranopia, or tritanopia."
        )

    # Convert BGR image to RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Normalize pixel values
    image_float = image_rgb.astype(np.float32) / 255.0

    # Apply transformation
    matrix = matrices[cvd_type]

    simulated = np.dot(image_float, matrix.T)

    # Keep values between 0 and 1
    simulated = np.clip(simulated, 0, 1)

    # Convert back to 8-bit image
    simulated = (simulated * 255).astype(np.uint8)

    return simulated
