"""
pattern_renderer.py
Percepta - Accessible Chart Reconstruction Module

Purpose:
    Colorblind users often can't distinguish chart series by color alone
    (e.g. red vs green bars look identical to someone with deuteranopia).
    This module fixes that by giving every series a DISTINCT visual
    identity using:
        - Hatch patterns (diagonal lines, dots, crosshatch) for bar charts
        - Distinct marker shapes (circle, triangle, square, star...) for
          scatter/line charts
        - Distinct line styles (solid, dashed, dotted) for line charts

    This can slot in as part of Developer 3's "render patterned
    alternative charts" step, or run standalone to test/demo the
    technique on its own.

Input contract:
    Simple Python data (labels + values per series) - this module does
    NOT need the raw image array from Developer 1. It's meant to redraw
    a NEW accessible version of a chart once you know what data/series
    the original chart represented.

Dependencies:
    matplotlib
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for scripts/servers
import matplotlib.pyplot as plt
import numpy as np


# A fixed, repeatable set of hatch patterns for bar charts.
# Cycles through if there are more series than patterns.
HATCH_PATTERNS = ["//", "\\\\", "xx", "..", "++", "oo", "**", "--"]

# A fixed set of marker shapes for scatter/line charts.
MARKER_SHAPES = ["o", "^", "s", "D", "P", "X", "*", "v"]

# A fixed set of line styles for line charts.
LINE_STYLES = ["-", "--", "-.", ":"]

# Colorblind-safe palette (Okabe-Ito palette - widely used standard).
# Even though shapes/patterns carry the real meaning here, using a
# safe palette on top gives an extra layer of accessibility.
SAFE_PALETTE = [
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#000000",  # black
]


def render_accessible_bar_chart(
    categories: list,
    series_dict: dict,
    title: str = "Accessible Bar Chart",
    output_path: str = "accessible_bar_chart.png",
) -> str:
    """
    Render a grouped bar chart where every series is distinguishable by
    HATCH PATTERN + color, not color alone.

    Args:
        categories: list of category labels for the x-axis,
                    e.g. ["Q1", "Q2", "Q3", "Q4"]
        series_dict: dict of {series_name: [values...]}, e.g.
                     {"Product A": [10, 20, 15, 30], "Product B": [5, 25, 20, 10]}
        title: chart title
        output_path: where to save the PNG

    Returns:
        The output_path the chart was saved to.
    """
    num_series = len(series_dict)
    num_categories = len(categories)
    x = np.arange(num_categories)
    bar_width = 0.8 / num_series

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, (series_name, values) in enumerate(series_dict.items()):
        if len(values) != num_categories:
            raise ValueError(
                f"Series '{series_name}' has {len(values)} values, "
                f"expected {num_categories} to match categories."
            )
        offset = (i - num_series / 2) * bar_width + bar_width / 2
        ax.bar(
            x + offset,
            values,
            width=bar_width,
            label=series_name,
            color=SAFE_PALETTE[i % len(SAFE_PALETTE)],
            hatch=HATCH_PATTERNS[i % len(HATCH_PATTERNS)],
            edgecolor="black",
            linewidth=0.8,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


def render_accessible_line_chart(
    x_values: list,
    series_dict: dict,
    title: str = "Accessible Line Chart",
    output_path: str = "accessible_line_chart.png",
) -> str:
    """
    Render a line chart where every series is distinguishable by
    MARKER SHAPE + LINE STYLE + color, not color alone.

    Args:
        x_values: shared x-axis values, e.g. ["Jan", "Feb", "Mar"]
        series_dict: dict of {series_name: [values...]}
        title: chart title
        output_path: where to save the PNG

    Returns:
        The output_path the chart was saved to.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    for i, (series_name, values) in enumerate(series_dict.items()):
        ax.plot(
            x_values,
            values,
            label=series_name,
            color=SAFE_PALETTE[i % len(SAFE_PALETTE)],
            marker=MARKER_SHAPES[i % len(MARKER_SHAPES)],
            linestyle=LINE_STYLES[i % len(LINE_STYLES)],
            markersize=8,
            linewidth=2,
        )

    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


def render_accessible_scatter_chart(
    series_dict: dict,
    title: str = "Accessible Scatter Chart",
    output_path: str = "accessible_scatter_chart.png",
) -> str:
    """
    Render a scatter chart where every series is distinguishable by
    MARKER SHAPE + color, not color alone.

    Args:
        series_dict: dict of {series_name: (x_values, y_values)}, e.g.
                     {"Group A": ([1,2,3], [10,15,9]), "Group B": ([1,2,3], [5,8,12])}
        title: chart title
        output_path: where to save the PNG

    Returns:
        The output_path the chart was saved to.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    for i, (series_name, (xs, ys)) in enumerate(series_dict.items()):
        ax.scatter(
            xs,
            ys,
            label=series_name,
            color=SAFE_PALETTE[i % len(SAFE_PALETTE)],
            marker=MARKER_SHAPES[i % len(MARKER_SHAPES)],
            s=100,
            edgecolor="black",
            linewidth=0.5,
        )

    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


if __name__ == "__main__":
    # Smoke test - generates one of each chart type so you can visually
    # confirm patterns/shapes render correctly.

    bar_path = render_accessible_bar_chart(
        categories=["Q1", "Q2", "Q3", "Q4"],
        series_dict={
            "Product A": [10, 20, 15, 30],
            "Product B": [5, 25, 20, 10],
            "Product C": [15, 10, 25, 20],
        },
        title="Quarterly Sales (Accessible)",
        output_path="test_bar_chart.png",
    )
    print(f"Bar chart saved to: {bar_path}")

    line_path = render_accessible_line_chart(
        x_values=["Jan", "Feb", "Mar", "Apr", "May"],
        series_dict={
            "Revenue": [100, 120, 115, 140, 160],
            "Costs": [80, 85, 90, 95, 100],
        },
        title="Revenue vs Costs (Accessible)",
        output_path="test_line_chart.png",
    )
    print(f"Line chart saved to: {line_path}")

    scatter_path = render_accessible_scatter_chart(
        series_dict={
            "Group A": ([1, 2, 3, 4], [10, 15, 9, 12]),
            "Group B": ([1, 2, 3, 4], [5, 8, 12, 7]),
        },
        title="Group Comparison (Accessible)",
        output_path="test_scatter_chart.png",
    )
    print(f"Scatter chart saved to: {scatter_path}")
