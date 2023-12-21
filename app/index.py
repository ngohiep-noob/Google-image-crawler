import streamlit as st

from search_page import render_search_page

sidebar = st.sidebar
page = sidebar.radio("Choose a page", ["Search", "Manage"])
sidebar.title("Image retrieval application")

if page == "Search":
    sidebar.subheader("Search page")
    render_search_page()


if page == "Manage":
    sidebar.subheader("Manage page")
