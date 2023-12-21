import streamlit as st
from PIL import Image
from itertools import cycle
from src.retriever import Retriever

retriever = Retriever()


def render_search_page():
    # Title
    st.title("Vietnam46Attr image retrieval application")

    # Devide 2 columns
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Query image")
        uploaded_file = st.file_uploader(
            "Drop file here", type=["png", "jpg"], accept_multiple_files=False
        )
        if uploaded_file is not None:
            query_image = Image.open(uploaded_file)
            st.image(query_image, caption="Retrieved image", use_column_width=True)
        num_images = st.selectbox(
            "Number of images:", [i for i in range(1, 100)], index=9
        )

    with col2:
        st.subheader("Retrieved images")
        cols = cycle(st.columns(3))

        if uploaded_file is not None:
            idx, _ = retriever.retrieve(query_image, num_images)
            for i, col in zip(idx, cols):
                img, path = retriever.get_view(i)
                landmark = path.parent.name
                landmark = landmark.replace("_", " ").title()
                img = img.resize((224, 224))
                col.image(img, caption=landmark, use_column_width=True)
