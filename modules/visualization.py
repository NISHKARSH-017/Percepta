import matplotlib.pyplot as plt
import pandas as pd


def create_accessible_bar_chart(
    df,
    category_column,
    value_column,
    title="Accessible Visualization"
):
    """
    Create an accessible bar chart using:
    - Colorblind-friendly colors
    - Different hatch patterns
    - Value labels
    - Clear text labels
    """

    # Colorblind-friendly palette
    colors = [
        "#0072B2",  # Blue
        "#E69F00",  # Orange
        "#009E73",  # Green
        "#CC79A7",  # Purple
        "#56B4E9",  # Light blue
        "#D55E00"   # Red-orange
    ]

    # Different patterns so meaning isn't dependent on color
    patterns = [
        "",
        "//",
        "xx",
        "..",
        "\\\\",
        "++"
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    categories = df[category_column].astype(str)
    values = df[value_column]

    bars = ax.bar(
        categories,
        values,
        color=[
            colors[i % len(colors)]
            for i in range(len(df))
        ],
        edgecolor="black",
        linewidth=1.2
    )

    # Add patterns
    for i, bar in enumerate(bars):
        bar.set_hatch(
            patterns[i % len(patterns)]
        )

    # Add value labels
    for bar, value in zip(bars, values):

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    # Titles and labels
    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        category_column,
        fontsize=12
    )

    ax.set_ylabel(
        value_column,
        fontsize=12
    )

    # Improve readability
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xticks(
        rotation=0,
        fontsize=10
    )

    plt.tight_layout()

    return fig
