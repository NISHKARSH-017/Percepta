"""
accessibility.py
Developer 2 - Analytics Engineer (Percepta)

Responsibilities:
    Cross-compare the dominant colors found by color_analyzer.py and flag
    two kinds of accessibility violations:
        1. Similar-color barriers: two colors close enough in RGB space
           that a color-blind viewer would see them as the same shade.
        2. Low-contrast barriers: two colors whose perceptual brightness
           is too close together, risking text washing out against its
           background.

Output contract (to Developer 3):
    {
        "issues": [ { ...issue dict... }, ... ],
        "color_map": [ (R, G, B), ... ],   # the dominant colors used
        "total_errors": int
    }
"""

from color_analyzer import get_dominant_colors, color_distance, perceptual_brightness

# Standard thresholds (tune these later if design/QA wants them stricter)
SIMILARITY_THRESHOLD = 60   # RGB distance below this = "looks the same"
CONTRAST_THRESHOLD = 40     # brightness difference below this = "low contrast"


def scan_for_accessibility_issues(image_array, num_colors: int = 5) -> dict:
    """
    Run the full diagnostic pipeline on an image array:
        1. Extract dominant colors.
        2. Compare every unique pair for similarity + contrast issues.
        3. Package results into a clean dictionary for Developer 3.

    Args:
        image_array: np.ndarray (H, W, 3), RGB, uint8 - passed in from
                     Developer 1's pipeline.
        num_colors: how many dominant colors to extract and compare.

    Returns:
        dict with keys "issues", "color_map", "total_errors".
    """
    dominant_colors = get_dominant_colors(image_array, num_colors=num_colors)
    issues = []

    # Compare every unique pair exactly once (i < j avoids duplicates
    # and comparing a color against itself)
    for i in range(len(dominant_colors)):
        for j in range(i + 1, len(dominant_colors)):
            color_a = dominant_colors[i]
            color_b = dominant_colors[j]

            distance = color_distance(color_a, color_b)
            brightness_a = perceptual_brightness(color_a)
            brightness_b = perceptual_brightness(color_b)
            brightness_diff = abs(brightness_a - brightness_b)

            # --- Check 1: colors too similar (color-blind confusion risk) ---
            if distance < SIMILARITY_THRESHOLD:
                issues.append({
                    "type": "similar_colors",
                    "colors": [color_a, color_b],
                    "distance": round(distance, 2),
                    "threshold": SIMILARITY_THRESHOLD,
                    "message": (
                        f"Colors {color_a} and {color_b} are too close "
                        f"(distance {distance:.2f} < {SIMILARITY_THRESHOLD}); "
                        "a color-blind viewer may see these as identical."
                    ),
                })

            # --- Check 2: low contrast (text/background washout risk) ---
            if brightness_diff < CONTRAST_THRESHOLD:
                issues.append({
                    "type": "low_contrast",
                    "colors": [color_a, color_b],
                    "brightness_difference": round(brightness_diff, 2),
                    "threshold": CONTRAST_THRESHOLD,
                    "message": (
                        f"Colors {color_a} and {color_b} have low contrast "
                        f"(difference {brightness_diff:.2f} < {CONTRAST_THRESHOLD}); "
                        "text may wash out against this background."
                    ),
                })

    # Deduplicate (in case a pair somehow got flagged twice - defensive)
    seen = set()
    deduped_issues = []
    for issue in issues:
        key = (issue["type"], tuple(sorted(issue["colors"])))
        if key not in seen:
            seen.add(key)
            deduped_issues.append(issue)

    return {
        "issues": deduped_issues,
        "color_map": dominant_colors,
        "total_errors": len(deduped_issues),
    }


if __name__ == "__main__":
    import numpy as np

    # Smoke test: red and green blocks are a classic deuteranopia trap -
    # they're far apart in raw RGB distance but should still trip contrast
    # checks depending on brightness. Adjust the test image to taste.
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    test_img[:, :50] = [200, 60, 60]    # dull red
    test_img[:, 50:] = [60, 200, 60]    # dull green

    result = scan_for_accessibility_issues(test_img, num_colors=2)
    print("Color map:", result["color_map"])
    print("Total errors:", result["total_errors"])
    for issue in result["issues"]:
        print("-", issue["message"])
