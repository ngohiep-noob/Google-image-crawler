import streamlit as st

def render_action_page():
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("<h3>Add new landmark</h3>", unsafe_allow_html=True)
        with st.form("add_landmark_form"):
            st.text("Enter landmark's name:")
            c1, c2 = st.columns([4, 1])
            with c1:
                landmark_name = st.text_input(label='label', label_visibility="collapsed")
            with c2:
                submit_btn = st.form_submit_button(label="Add")
            if submit_btn:
                # Process the form submission here (if needed)
                st.success(f"Landmark '{landmark_name}' added!")  


    with col2:
        option=["one", "two", "threee"]
        st.markdown("<h3>Add a new image to landmark</h3>", unsafe_allow_html=True)
        with st.form("add_img_form"):
            st.text("Choose landmark")
            st.selectbox(label="select", label_visibility="collapsed", options=option)
            st.file_uploader(
                "Drop file here", type=["png", "jpg"], accept_multiple_files=False
            )
            st.form_submit_button(label="Add")



