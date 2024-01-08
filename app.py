import streamlit as st
from pages.search_page.search_page import search_page
from pages.manage_page.manage_page import manage_page

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
        search_page()

if page == "Manage":
    sidebar.subheader("Manage page")
    manage_page()
