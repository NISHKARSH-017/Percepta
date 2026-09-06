def calculate_accessibility_score(analysis_result):
    """
    Calculate an accessibility score from 0 to 100.

    Starts at 100 and subtracts points
    depending on the severity of detected issues.
    """

    score = 100

    issues = analysis_result.get("issues", [])

    for issue in issues:

        severity = issue.get("severity", "Medium")

        if severity == "High":
            score -= 15

        elif severity == "Medium":
            score -= 8

        elif severity == "Low":
            score -= 4

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    # Determine a human-readable rating
    if score >= 90:
        rating = "Excellent"

    elif score >= 75:
        rating = "Good"

    elif score >= 50:
        rating = "Needs Improvement"

    else:
        rating = "Poor"

    return {
        "score": score,
        "rating": rating,
        "issue_count": len(issues)
    }


def get_score_color(score):
    """
    Return a color based on the accessibility score.
    """

    if score >= 90:
        return "#009E73"  # Green

    elif score >= 75:
        return "#E69F00"  # Orange

    elif score >= 50:
        return "#D55E00"  # Red-orange

    else:
        return "#D55E00"  # Red-orange


def get_score_message(score):
    """
    Return a simple explanation for the score.
    """

    if score >= 90:
        return "This visualization is highly accessible."

    elif score >= 75:
        return "This visualization is mostly accessible, but could be improved."

    elif score >= 50:
        return "This visualization has several accessibility issues."

    else:
        return "This visualization may be difficult to understand for people with CVD."
