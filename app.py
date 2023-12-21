import streamlit as st

from search_page import render_search_page

st.set_page_config(
    page_title="Vietnam46Attr IR",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)
sidebar = st.sidebar
page = sidebar.radio("Choose a page", ["Search", "Manage"])
sidebar.title("Image retrieval application")

if page == "Search":
    with st.container(border=True):
        sidebar.subheader("Search page")
        render_search_page()


if page == "Manage":
    sidebar.subheader("Manage page")
