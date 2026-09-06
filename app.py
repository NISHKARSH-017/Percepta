import io
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# ---------------------------------------------------------
# IMPORT TEAM BACKEND MODULES
# ---------------------------------------------------------
from modules.cvd_simulator import simulate_cvd
from modules.chart_processor import load_chart, resize_image
from modules.visualization import create_accessible_bar_chart
from modules.scoring import calculate_accessibility_score, get_score_color, get_score_message
from modules.ai import generate_explanation
from modules.color_analyzer import get_dominant_colors

# ---------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Percepta — Accessible Visualizations",
    page_icon="◉",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; margin-bottom: 0px; }
    .hero-subtitle { font-size: 18px; color: #475569; margin-bottom: 20px; }
    .score-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .score-val { font-size: 48px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">◉ Percepta</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-Powered Accessibility Engine for Universal Data Visualizations</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    st.write("Preview visualizations through calibrated Color Vision Deficiency (CVD) lenses.")
    cvd_choice = st.selectbox(
        "Select CVD Type:",
        ["Protanopia", "Deuteranopia", "Tritanopia"]
    )
    st.divider()
    st.info("Percepta automatically injects geometric shape cues (●, ▲, ■) and tactile hatch patterns so critical data never relies on color alone.")

# ---------------------------------------------------------
# HELPER: IMAGE-TO-CHART DATA CONVERTER
# ---------------------------------------------------------
def extract_data_from_image(image_array, num_categories=4):
    """
    Scans image pixels to isolate primary color segments and generates
    a structured table so dev3.py can redraw it with shapes and patterns.
    """
    colors = get_dominant_colors(image_array, num_colors=num_categories)
    pixels = np.array(image_array).reshape(-1, 3)
    counts = []
    labels = []
    
    for idx, col in enumerate(colors):
        dist = np.linalg.norm(pixels - np.array(col), axis=1)
        count = int(np.sum(dist < 50))
        counts.append(max(count, 15))
        labels.append(f"Metric {idx + 1}")

    return pd.DataFrame({
        "Category": labels,
        "Value": counts
    })

# ---------------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a chart snapshot (PNG, JPG) or raw tabular dataset (CSV):",
    type=["png", "jpg", "jpeg", "csv"]
)

if not uploaded_file:
    st.info("👋 Upload a chart image or CSV file above to begin the accessibility analysis and rebuild.")
    st.stop()

# =========================================================
# WORKFLOW A: CSV DATASET UPLOAD
# =========================================================
if uploaded_file.name.lower().endswith(".csv"):
    df = pd.read_csv(uploaded_file)
    st.success("CSV dataset loaded successfully!")

    with st.expander("📄 View Raw Dataset Preview", expanded=False):
        st.dataframe(df, use_container_width=True)

    cols = list(df.columns)
    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    categorical_cols = [c for c in cols if c not in numeric_cols]

    if not numeric_cols or not categorical_cols:
        st.error("Your CSV requires at least one text category column and one numeric column.")
        st.stop()

    c1, c2 = st.columns(2)
    with c1:
        cat_col = st.selectbox("Select Category Column:", categorical_cols)
    with c2:
        val_col = st.selectbox("Select Value Column:", numeric_cols)

    if st.button("🚀 Analyze & Generate Accessible Visualization", type="primary", use_container_width=True):
        st.divider()
        st.subheader("✅ Percepta Reconstructed Visualization")
        st.write("Dynamic multi-sensory visual cues applied: color-blind safe palettes, unique physical hatch patterns, and explicit numeric headers.")
        
        fig = create_accessible_chart(df, cat_col, val_col, title=f"Universal Accessible Breakdown ({cat_col})")
        st.pyplot(fig, use_container_width=True)

# =========================================================
# WORKFLOW B: IMAGE (PNG / JPG) UPLOAD
# =========================================================
else:
    # 1. Load image cleanly into memory
    pil_img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(pil_img)

    st.success("Chart image loaded successfully!")

    # 2. CVD Simulation Side-by-Side Comparison
    st.divider()
    st.subheader(f"1. Color Vision Deficiency Simulation ({cvd_choice})")
    
    simulated_img = simulate_cvd(img_array, cvd_choice.lower())
    
    col_orig, col_sim = st.columns(2)
    with col_orig:
        st.write("**Original Visualization View**")
        st.image(img_array, use_container_width=True)
    with col_sim:
        st.write(f"**Simulated {cvd_choice} Lens View**")
        st.image(simulated_img, use_container_width=True)

    # 3. Analytics & Issue Detection
    with st.spinner("Running color cluster and contrast scans..."):
        analysis_data = scan_for_accessibility_issues(img_array)
        score_data = calculate_score(analysis_data)
        explanation_data = generate_accessibility_explanation(analysis_data, score_data)

    # 4. Accessibility Score and Metrics Card
    st.divider()
    st.subheader("2. Visual Accessibility Diagnostics")
    
    m1, m2 = st.columns([1, 2])
    with m1:
        score_val = score_data["score"]
        rating_label = score_data["rating"]
        score_color = get_score_ui_color(score_val)
        
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 14px; color: #64748b; font-weight: 600;">ACCESSIBILITY CLARITY SCORE</div>
            <div class="score-val" style="color: {score_color};">{score_val}/100</div>
            <div style="font-weight: 700; font-size: 18px; color: #1e293b;">{rating_label}</div>
            <p style="font-size: 13px; color: #64748b; margin-top: 8px;">{get_score_ui_message(score_val)}</p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.write("#### ⚠️ Detected Design Violations")
        if not analysis_data["issues"]:
            st.success("✓ No critical color overlap or low-contrast barriers detected.")
        else:
            for issue in analysis_data["issues"]:
                st.warning(f"**[{issue['type'].replace('_', ' ').title()}]**: {issue['message']}")

    # 5. Core Rebuild: Convert Image to Shapes & Patterns
    st.divider()
    st.subheader("3. Percepta Reconstructed Accessible Visualization")
    st.write("Because flat images rely on color alone, Percepta converts the extracted color clusters into an accessible chart with **unique hatch patterns (`//`, `xx`, `..`)**, **geometric symbol encodings**, and **explicit labels**.")

    detected_df = extract_data_from_image(img_array)
    rebuilt_fig = create_accessible_chart(
        df=detected_df,
        category_col="Category",
        value_col="Value",
        title=f"Percepta Universal Multi-Coded Reconstruction"
    )
    st.pyplot(rebuilt_fig, use_container_width=True)

    # 6. AI Explanation Breakdown
    st.divider()
    st.subheader("✨ Automated Accessibility Insights")
    st.info(explanation_data["summary"])
    
    st.write("##### Key Design Adjustments Applied:")
    for imp in explanation_data["improvements"]:
        st.markdown(f"- {imp}")
    
    st.write("##### Design Recommendation:")
    st.caption(explanation_data["recommendation"])

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()
st.caption("Percepta — Ensuring no critical data is missed due to color alone.")


