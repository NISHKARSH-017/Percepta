import streamlit as st

st.set_page_config(
    page_title="Percepta",
    page_icon="◉",
    layout="wide"
)

st.title("◉ Percepta")
st.subheader("AI-Powered Accessibility for Data Visualizations")

st.write(
    "Make data visualizations understandable for everyone."
)

uploaded_file = st.file_uploader(
    "Upload your chart or dataset",
    type=["png", "jpg", "jpeg", "csv"]
)

if uploaded_file:
    st.success("File uploaded successfully!")
