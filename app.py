import streamlit as st
from PIL import Image

sidebar = st.sidebar
page = sidebar.radio("Choose a page", ["Search", "Manage"])

if page == "Search":
    # Title
    st.title('Image Retrieval Application')
    # Title
    st.title('Image Retrieval Application')

    # Devide 2 columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Query Image')
        uploaded_file = st.file_uploader("Drop file here", type=["png", "jpg"], accept_multiple_files=False)
        if uploaded_file is not None:
            query_image = Image.open(uploaded_file)
            st.image(query_image, caption='Retrieved Imaged', use_column_width=True)
        num_images = st.selectbox('Number of images:', [i for i in range(1, 50)])

    with col2:
        st.subheader('Retrieved Images')
        if uploaded_file is not None:  
            for i in range(0, num_images, 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < num_images:
                        with cols[j]:
                            st.image(query_image, caption='i', use_column_width=True)

if page == "Manage":
    sidebar.subheader("Manage")


