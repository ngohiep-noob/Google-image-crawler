import streamlit as st
from src.main import manager
from PIL import Image


def render_action_page():
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("<h3>Add new landmark</h3>", unsafe_allow_html=True)
        with st.form("add_landmark_form"):
            st.text("Enter landmark's name:")
            c1, c2 = st.columns([4, 1])
            with c1:
                landmark_name = st.text_input(
                    label="label", label_visibility="collapsed"
                )
            with c2:
                submit_btn = st.form_submit_button(label="Add")
            if submit_btn:
                try:
                    manager.create_landmark(landmark_name)
                    st.success(f"Landmark '{landmark_name}' added!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    with col2:
        option = manager.get_landmark_list()
        st.markdown("<h3>Add a new image to landmark</h3>", unsafe_allow_html=True)
        with st.form("add_img_form"):
            st.text("Choose landmark")
            selected_landmark = st.selectbox(
                label="select", label_visibility="collapsed", options=option
            )
            upload_list = st.file_uploader(
                "Drop images here", type=["png", "jpg"], accept_multiple_files=True
            )

            submitted = st.form_submit_button(label="Add")

            if submitted:
                # Process the form submission here (if needed)
                if upload_list is not None and len(upload_list) > 0:
                    imgs = [Image.open(img) for img in upload_list]
                    try:
                        manager.add_images_to_landmark(selected_landmark, imgs)
                        st.success(f"Added {len(imgs)} images to {selected_landmark}")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.error("No image uploaded!")
