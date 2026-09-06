"""
modules/branding.py — Percepta visual identity.

Usage in app.py:
    from modules.branding import inject_theme, render_hero, render_sidebar_brand, BRAND_PALETTE, PAGE_ICON

Call inject_theme() once, immediately after st.set_page_config().
Call render_hero() where you want the logo + title block to appear.
BRAND_PALETTE can be imported by chart-generating modules
(visualization.py, chart_rebuilder.py, etc.) so bars/lines use
colorblind-safe colors instead of matplotlib defaults.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Colorblind-safe palette (Okabe-Ito). Thematically correct for a CVD tool —
# use this anywhere a chart color is chosen.
# ---------------------------------------------------------------------------
BRAND_PALETTE = [
    "#0072B2",  # blue        (primary)
    "#E69F00",  # orange      (accent)
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#56B4E9",  # sky blue
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
]

PRIMARY = BRAND_PALETTE[0]
ACCENT = BRAND_PALETTE[1]
INK = "#111827"
MUTED = "#64748b"
BG = "#f8fafc"

PAGE_ICON = "◉"  # safe emoji/glyph fallback — no file dependency


def _logo_svg(size: int = 44) -> str:
    """
    Inline SVG logomark: a stylised eye made of a two-tone gradient arc,
    on-brand for a CVD-accessibility product. No external file needed,
    so it can't 404 or crash st.logo() if assets/ doesn't exist yet.
    """
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 64 64"
         xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;">
        <defs>
            <linearGradient id="perceptaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{PRIMARY}"/>
                <stop offset="100%" stop-color="{ACCENT}"/>
            </linearGradient>
        </defs>
        <path d="M4 32 C 16 8, 48 8, 60 32 C 48 56, 16 56, 4 32 Z"
              fill="none" stroke="url(#perceptaGrad)" stroke-width="4.5" stroke-linecap="round"/>
        <circle cx="32" cy="32" r="10" fill="url(#perceptaGrad)"/>
        <circle cx="28.5" cy="28.5" r="3" fill="#ffffff" opacity="0.85"/>
    </svg>
    """


def render_hero() -> None:
    """Renders the logo + title + tagline hero block."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">
                {_logo_svg(48)} PERCEPTA
            </div>
            <div class="hero-subtitle">
                AI-Powered Accessibility for Data Visualizations
            </div>
            <div class="tagline">
                Detect • Simulate • Improve • Explain
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    """Renders a compact logo + name at the top of the sidebar."""
    st.sidebar.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            {_logo_svg(30)}
            <span style="font-size:22px; font-weight:800; color:{INK};">Percepta</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_theme() -> None:
    """Injects global CSS. Call once, right after st.set_page_config()."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Space Grotesk', sans-serif;
        }}

        .main {{
            background-color: {BG};
        }}

        /* ---------- Hero ---------- */
        .hero {{
            padding: 40px 20px 30px 20px;
            text-align: center;
        }}

        .hero-title {{
            font-size: 46px;
            font-weight: 800;
            color: {INK};
            margin-bottom: 5px;
            letter-spacing: -0.5px;
        }}

        .hero-subtitle {{
            font-size: 20px;
            color: {MUTED};
            margin-bottom: 6px;
        }}

        .tagline {{
            font-size: 15px;
            font-weight: 600;
            background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }}

        /* ---------- Upload box ---------- */
        .upload-box {{
            padding: 30px;
            border-radius: 16px;
            background-color: white;
            border: 2px dashed {PRIMARY}66;
            text-align: center;
            transition: border-color 0.2s ease;
        }}

        .upload-box:hover {{
            border-color: {PRIMARY};
        }}

        /* ---------- Section titles ---------- */
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            color: {INK};
            margin-top: 25px;
            border-left: 4px solid {PRIMARY};
            padding-left: 10px;
        }}

        /* ---------- Status boxes ---------- */
        .issue-box {{
            padding: 18px;
            border-radius: 12px;
            background-color: #fff7ed;
            border-left: 5px solid {ACCENT};
            margin-bottom: 10px;
        }}

        .success-box {{
            padding: 18px;
            border-radius: 12px;
            background-color: #ecfdf5;
            border-left: 5px solid #009E73;
        }}

        .score-box {{
            padding: 25px;
            border-radius: 16px;
            background-color: white;
            text-align: center;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        }}

        .score-number {{
            font-size: 52px;
            font-weight: 800;
            background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            padding: 0.6rem 1.4rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}

        div.stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 16px {PRIMARY}40;
        }}

        /* ---------- File uploader ---------- */
        [data-testid="stFileUploaderDropzone"] {{
            border: 1.5px dashed {PRIMARY}88;
            border-radius: 12px;
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }}

        /* ---------- Metrics ---------- */
        div[data-testid="stMetric"] {{
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 10px 6px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
