
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

from modules.cvd import simulate_cvd
from modules.analysis import analyze_colors
from modules.visualization import create_accessible_bar_chart
from modules.scoring import (
    calculate_accessibility_score,
    get_score_color,
    get_score_message
)
from modules.ai import generate_explanation


def df_to_image(df, category_column, value_column):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df[category_column].astype(str), df[value_column])
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)



# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Percepta",
    page_icon="◉",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #f8fafc;
    }

    .hero {
        padding: 40px 20px 30px 20px;
        text-align: center;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 20px;
        color: #64748b;
        margin-bottom: 10px;
    }

    .tagline {
        font-size: 15px;
        color: #475569;
    }

    .upload-box {
        padding: 30px;
        border-radius: 16px;
        background-color: white;
        border: 2px dashed #94a3b8;
        text-align: center;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
    }

    .issue-box {
        padding: 18px;
        border-radius: 12px;
        background-color: #fff7ed;
        border-left: 5px solid #f97316;
        margin-bottom: 10px;
    }

    .success-box {
        padding: 18px;
        border-radius: 12px;
        background-color: #ecfdf5;
        border-left: 5px solid #10b981;
    }

    .score-box {
        padding: 25px;
        border-radius: 16px;
        background-color: white;
        text-align: center;
        border: 1px solid #e2e8f0;
    }

    .score-number {
        font-size: 52px;
        font-weight: 800;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-title">
        ◉ PERCEPTA
    </div>

    <div class="hero-subtitle">
        AI-Powered Accessibility for Data Visualizations
    </div>

    <div class="tagline">
        Detect • Simulate • Improve • Explain
    </div>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("Percepta")

    st.write(
        "Make your data visualizations more accessible "
        "for people with Color Vision Deficiency."
    )

    st.divider()

    st.subheader("Supported CVD Types")

    cvd_type = st.selectbox(
        "Choose simulation",
        [
            "Protanopia",
            "Deuteranopia",
            "Tritanopia"
        ]
    )

    st.divider()

    st.info(
        "Percepta analyzes colors, contrast, and visual "
        "encoding to identify accessibility problems."
    )


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">1. Upload your visualization</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a chart or dataset",
    type=["png", "jpg", "jpeg", "csv"]
)


# ---------------------------------------------------------
# WHEN NO FILE IS UPLOADED
# ---------------------------------------------------------

if uploaded_file is None:

    st.markdown("""
    <div class="upload-box">

        <h2>📊 Upload your chart or dataset</h2>

        <p>
        Percepta will analyze your visualization,
        simulate Color Vision Deficiency,
        and generate an accessible version.
        </p>

        <p>
        <b>Supported:</b> PNG, JPG, JPEG, CSV
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ---------------------------------------------------------
# PROCESS CSV
# ---------------------------------------------------------

if uploaded_file.name.lower().endswith(".csv"):

    try:

        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        st.markdown(
            '<div class="section-title">Dataset Preview</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # Select columns
        columns = list(df.columns)

        if len(columns) >= 2:

            col1, col2 = st.columns(2)

            with col1:

                category_column = st.selectbox(
                    "Category column",
                    columns
                )

            with col2:

                numeric_columns = [
                    col for col in columns
                    if pd.api.types.is_numeric_dtype(df[col])
                ]

                if numeric_columns:

                    value_column = st.selectbox(
                        "Value column",
                        numeric_columns
                    )

                else:

                    st.error(
                        "Your CSV needs at least one numeric column."
                    )

                    st.stop()

            analyze_button = st.button(
                "🔍 Analyze & Improve Visualization",
                type="primary",
                use_container_width=True
            )

            if analyze_button:

                st.session_state["csv_analyzed"] = True
                st.session_state["category_column"] = category_column
                st.session_state["value_column"] = value_column
                st.session_state["df"] = df


        else:

            st.error(
                "Please upload a CSV with at least two columns."
            )


    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# ---------------------------------------------------------
# PROCESS IMAGE
# ---------------------------------------------------------

else:

    image = Image.open(uploaded_file)

    st.success("Image uploaded successfully!")

    st.markdown(
        '<div class="section-title">Original Visualization</div>',
        unsafe_allow_html=True
    )

    st.image(
        image,
        use_container_width=True
    )

    analyze_button = st.button(
        "🔍 Analyze Visualization",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        st.session_state["image_analyzed"] = True
        st.session_state["uploaded_image"] = image


# ---------------------------------------------------------
# CSV ANALYSIS RESULTS
# ---------------------------------------------------------

if st.session_state.get("csv_analyzed", False):

    df = st.session_state["df"]

    category_column = st.session_state["category_column"]
    value_column = st.session_state["value_column"]

    st.divider()

    st.markdown(
        '<div class="section-title">2. Accessibility Analysis</div>',
        unsafe_allow_html=True
    )

    # Create visualization
    original_fig = create_accessible_bar_chart(
        df,
        category_column,
        value_column,
        "Visualization"
    )

    st.pyplot(
        original_fig,
        use_container_width=True
    )

    # Analyze generated chart
    analysis_result = analyze_colors(
        df_to_image(df, category_column, value_column)
    )

    score_result = calculate_accessibility_score(
        analysis_result
    )

    explanation = generate_explanation(
        analysis_result,
        score_result
    )

    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">3. Accessibility Score</div>',
        unsafe_allow_html=True
    )

    score = score_result["score"]
    rating = score_result["rating"]

    score_color = get_score_color(score)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Accessibility Score",
            f"{score}/100"
        )

    with col2:

        st.metric(
            "Rating",
            rating
        )

    with col3:

        st.metric(
            "Issues Detected",
            score_result["issue_count"]
        )

    st.progress(
        score / 100
    )

    st.caption(
        get_score_message(score)
    )

    # -----------------------------------------------------
    # ISSUES
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">4. Detected Issues</div>',
        unsafe_allow_html=True
    )

    if analysis_result["issues"]:

        for issue in analysis_result["issues"]:

            st.warning(
                f"{issue['type']}: {issue['message']}"
            )

    else:

        st.success(
            "No major accessibility issues detected."
        )

    # -----------------------------------------------------
    # IMPROVED VISUALIZATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">5. Improved Visualization</div>',
        unsafe_allow_html=True
    )

    improved_fig = create_accessible_bar_chart(
        df,
        category_column,
        value_column,
        "Percepta Accessible Visualization"
    )

    st.pyplot(
        improved_fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # AI EXPLANATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">6. ✨ AI Explanation</div>',
        unsafe_allow_html=True
    )

    st.info(
        explanation["summary"]
    )

    st.subheader("What Percepta improved")

    for improvement in explanation["improvements"]:

        st.write(
            f"✓ {improvement}"
        )

    st.subheader("Recommendation")

    st.write(
        explanation["recommendation"]
    )


# ---------------------------------------------------------
# IMAGE ANALYSIS RESULTS
# ---------------------------------------------------------

if st.session_state.get("image_analyzed", False):

    image = st.session_state["uploaded_image"]

    st.divider()

    st.markdown(
        '<div class="section-title">2. CVD Simulation</div>',
        unsafe_allow_html=True
    )

    # Convert selected option to lowercase
    selected_cvd = cvd_type.lower()

    try:

        simulated_image = simulate_cvd(
            image,
            selected_cvd
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Original")

            st.image(
                image,
                use_container_width=True
            )

        with col2:

            st.subheader(
                f"{cvd_type} Simulation"
            )

            st.image(
                simulated_image,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"CVD simulation could not be completed: {e}"
        )

    # Analyze image
    analysis_result = analyze_colors(image)

    score_result = calculate_accessibility_score(
        analysis_result
    )

    explanation = generate_explanation(
        analysis_result,
        score_result
    )

    st.markdown(
        '<div class="section-title">3. Accessibility Report</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Accessibility Score",
            f"{score_result['score']}/100"
        )

    with col2:

        st.metric(
            "Rating",
            score_result["rating"]
        )

    with col3:

        st.metric(
            "Issues Detected",
            score_result["issue_count"]
        )

    st.progress(
        score_result["score"] / 100
    )

    if analysis_result["issues"]:

        st.subheader("⚠ Detected Issues")

        for issue in analysis_result["issues"]:

            st.warning(
                f"{issue['type']}: {issue['message']}"
            )

    else:

        st.success(
            "✓ No major accessibility issues detected."
        )

    st.subheader("✨ AI Explanation")

    st.info(
        explanation["summary"]
    )

    for improvement in explanation["improvements"]:

        st.write(
            f"✓ {improvement}"
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Percepta — Making data visualizations accessible for everyone."
)
