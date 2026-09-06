def calculate_score(analysis_result):
    """
    Deducts quality metrics out of a baseline safety score of 100 points
    based on the design violations caught by Developer 2.
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

    # Keep score between 0 and 100 boundaries
    score = max(0, min(100, score))
    
    if score >= 90:
        rating = "Excellent"
    elif score >= 75:
        rating = "Good"
    elif score >= 50:
        rating = "Needs Improvement"
    else:
        rating = "Poor"

    return {"score": score, "rating": rating, "issue_count": len(issues)}


def get_score_ui_color(score):
    """
    Returns high-contrast Hex codes to dynamically color the UI cards.
    """
    if score >= 90:
        return "#009E73"  # Accessible Green
    elif score >= 75:
        return "#E69F00"  # Orange
    else:
        return "#D55E00"  # Red-Orange


def get_score_ui_message(score):
    """
    Returns simple summary string messages to print under the metrics panel.
    """
    if score >= 90:
        return "This visualization is highly accessible."
    elif score >= 75:
        return "This visualization is mostly accessible, but could be improved."
    else:
        return "This visualization may be difficult to interpret for individuals with CVD."
