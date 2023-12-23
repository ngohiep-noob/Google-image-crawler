import streamlit as st
from PIL import Image
from itertools import cycle
from src.main import retriever
from pathlib import Path
import requests


def image_from_url(url):
    """Fetches an image from the given URL and returns it as a PIL Image."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        img = Image.open(response.raw)
        return img
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image from URL: {e}")
        return None


def search_page():
    # Title
    st.title("Vietnam46Attr image retrieval application")

    # divide 2 columns
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.subheader("Query image")

        input_options = st.selectbox(
            "Input options:",
            ["Upload image", "Enter URL"],
        )
        query_image = None

        if input_options == "Upload image":
            uploaded_file = st.file_uploader(
                "Drop file here", type=["png", "jpg"], accept_multiple_files=False
            )
            if uploaded_file is not None:
                query_image = Image.open(uploaded_file)

        else:
            url = st.text_input("Or enter URL here")
            if url:
                query_image = image_from_url(url)

        if query_image is not None:
            st.image(query_image, caption="Query image", use_column_width=True)

        num_images = st.selectbox(
            "Number of images:", [i for i in range(1, 100)], index=9
        )

    with col2:
        st.subheader("Retrieved images")
        cols = cycle(st.columns(3))

        if query_image is not None:
            idx, _ = retriever.retrieve(query_image, num_images)
            for i, col in zip(idx, cols):
                img, path = retriever.get_view(i)
                landmark = Path(path).parent.name
                landmark = landmark.replace("_", " ").title()
                img = img.resize((224, 224))
                col.image(img, caption=landmark, use_column_width=True)
