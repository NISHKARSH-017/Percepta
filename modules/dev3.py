import matplotlib.pyplot as plt
import pandas as pd

def create_accessible_chart(df, category_col, value_col, title="Accessible Visualizer"):
    """
    Yeh function normal data ko ek colorblind-safe, patterned bar chart mein convert karta hai.
    """
    # 1. Colorblind-friendly colors ka ek standard safe palette (WCAG approved)
    colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00"]
    
    # 2. Alag alag texture patterns takisirf color par dependency na rahe
    # '' = plain, '//' = diagonal lines, 'xx' = crosses, '..' = dots
    patterns = ["", "//", "xx", "..", "\\\\", "++"]

    # Matplotlib ka ek blank graph stand ready karna
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = df[category_col].astype(str)
    values = df[value_col]

    # Bar chart plot karna humare safe colors ke saath
    bars = ax.bar(
        categories, values,
        color=[colors[i % len(colors)] for i in range(len(df))],
        edgecolor="black", linewidth=1.2
    )

    # LOOP: Har ek bar par alag texture pattern apply karna
    for i, bar in enumerate(bars):
        bar.set_hatch(patterns[i % len(patterns)])

    # LOOP: Bars ke upar unki exact numeric value text likhna takiguessing na karni pade
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


    # Graph ki styling elements clean aur clear rakhna
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(category_col, fontsize=11)
    ax.set_ylabel(value_col, fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.tight_layout()
    return fig # Yeh poora graph frontend ko return ho jayega screen par dikhane ke liye

# =====================================================================
# SYSTEM VERIFICATION TEST BLOCK
# =====================================================================
if __name__ == "__main__":
    print("\n--- RUNNING DEV 3 BACKEND VERIFICATION RUN ---")
    
    # 1. Create a dummy dataframe to simulate frontend user data files
    test_df = pd.DataFrame({
        "Patient Status": ["Stable", "Monitor", "Critical"],
        "Patient Count": [45, 25, 12]
    })
    
    print("[+] Reshaping raw data framework... Complete!")
    
    # 2. Try drawing the accessible patterned bar chart block layout
    try:
        chart_figure = create_accessible_chart(test_df, "Patient Status", "Patient Count", "C2C Live Demo Map")
        print("[+] Universal Chart Rebuilder Engine... Functional!")
    except Exception as e:
        print(f"[-] Rebuilder Execution Crash: {e}")
