def generate_explanation(analysis_result, score_result):
    """
    Generate an accessibility explanation.

    This version creates a clear explanation from the
    analysis results. It can later be connected to an
    LLM API for more advanced explanations.
    """

    score = score_result.get("score", 0)
    rating = score_result.get("rating", "Unknown")

    issues = analysis_result.get("issues", [])

    # No issues detected
    if not issues:

        return {
            "summary": (
                "Percepta did not detect major color or "
                "contrast problems in this visualization."
            ),
            "improvements": [
                "The visualization has good color separation.",
                "The visualization can be understood without major difficulty."
            ],
            "recommendation": (
                "The visualization already has a good level of accessibility."
            )
        }

    # Collect issue types
    issue_types = set()

    for issue in issues:
        issue_types.add(issue.get("type", ""))

    improvements = []

    if "Similar Colors" in issue_types:
        improvements.append(
            "Used more distinguishable colors so categories are easier to identify."
        )

    if "Low Contrast" in issue_types:
        improvements.append(
            "Improved contrast between visual elements and the background."
        )

    # Add redundant visual cues
    improvements.append(
        "Added patterns and visual differences so information does not rely only on color."
    )

    improvements.append(
        "Added clear labels to make categories easier to understand."
    )

    # Create summary
    if score < 50:
        summary = (
            "Percepta found several significant accessibility problems. "
            "The visualization may be difficult to interpret for people "
            "with Color Vision Deficiency."
        )

    elif score < 75:
        summary = (
            "Percepta found some accessibility problems. "
            "Several visual elements could be difficult to distinguish "
            "for people with Color Vision Deficiency."
        )

    else:
        summary = (
            "Percepta found a few accessibility issues, but the "
            "visualization is generally understandable."
        )

    recommendation = (
        "Percepta recommends using multiple visual cues such as "
        "color, patterns, shapes, labels, and contrast instead of "
        "using color alone."
    )

    return {
        "summary": summary,
        "improvements": improvements,
        "recommendation": recommendation
    }
