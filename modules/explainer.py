def generate_accessibility_explanation(analysis_result, score_result):
    """
    Generates plain-language text summaries detailing the accessibility 
    improvements made by the platform.
    """
    score = score_result.get("score", 0)
    issues = analysis_result.get("issues", [])

    if not issues:
        return {
            "summary": "Percepta did not detect major color or contrast problems in this visualization.",
            "improvements": ["Maintains good color barrier separation across sections."],
            "recommendation": "The current dashboard layout matches accessible criteria parameters."
        }

    types = {iss.get("type", "") for iss in issues}
    improvements = []

    if "Similar Colors" in types:
        improvements.append("Expanded color space distribution distances between categories.")
    if "Low Contrast" in types:
        improvements.append("Boosted absolute background contrast depth configurations.")

    improvements.extend([
        "Applied distinct physical pattern variations (hatching) to remove single points of failure.",
        "Attached readable text numeric labels right over chart data nodes."
    ])

    if score < 50:
        summary = "Significant layout barriers spotted. Individuals with CVD will find this chart extremely difficult to read without our design layers."
    elif score < 75:
        summary = "Moderate design concerns detected. Certain visual clusters blend together under CVD lenses."
    else:
        summary = "Minor issues flagged, but structural legibility remains solid."

    return {
        "summary": summary,
        "improvements": improvements,
        "recommendation": "Percepta recommends integrating shapes, text labels, and unique pattern fills alongside standard color codes."
    }
