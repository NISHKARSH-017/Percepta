import matplotlib.pyplot as plt
import pandas as pd

def create_accessible_chart(df, category_col, value_col, title="Accessible Visualizer"):
    """
    UNIVERSAL BACKEND ENGINE: Dynamically assigns geometric symbols and 
    texture patterns to ANY number of custom categories uploaded by the user.
    """
    # 1. Pool of highly distinct universal geometric symbols
    shape_pool = ["●", "▲", "■", "◆", "▼", "★", "⬢", "⬪", "🃏", "⎔"]
    
    # Get all unique categories present in the user's uploaded dataset
    unique_categories = df[category_col].unique().tolist()
    
    # Dynamically build a map matching each unique category to a shape from our pool
    dynamic_shape_rules = {}
    for index, category in enumerate(unique_categories):
        # Use modulo (%) safety cycling so we never run out of shapes
        symbol = shape_pool[index % len(shape_pool)]
        dynamic_shape_rules[category] = f"{symbol} {category}"
        
    # Apply our dynamic text-shape mapping down the dataset rows
    df['Accessible_Axis_Label'] = df[category_col].map(dynamic_shape_rules)

    # 2. Vetted color-blind safe theme colors (WCAG compliant palette)
    colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#56B4E9"]
    
    # 3. Dynamic texture patterns pool
    patterns = ["", "//", "xx", "..", "\\\\", "++", "||", "--"]

    # Initialize the Matplotlib figure canvas
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = df['Accessible_Axis_Label'].astype(str)
    values = df[value_col]

    # Render the bar chart using safety loops
    bars = ax.bar(
        categories, values,
        color=[colors[idx % len(colors)] for idx in range(len(df))],
        edgecolor="black", linewidth=1.2
    )

    # LOOP 1: Apply unique physical textures dynamically by cycling the list
    for idx, bar in enumerate(bars):
        bar.set_hatch(patterns[idx % len(patterns)])

    # LOOP 2: Place float padding numbers clearly above each bar row
    for bar, val in zip(bars, values):
        y_position = bar.get_height() * 1.01  
        ax.text(
            bar.get_x() + bar.get_width()/2, 
            y_position,
            str(val), 
            ha="center", 
            va="bottom", 
            fontsize=10, 
            fontweight="bold"
        )

    # Clean UI styling rules
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(category_col, fontsize=11)
    ax.set_ylabel(value_col, fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.tight_layout()
    return fig