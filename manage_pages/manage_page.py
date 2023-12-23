import streamlit as st
from streamlit_option_menu import option_menu
from manage_pages.collection_page import render_collection_page
from manage_pages.action_page import render_action_page

def render_manage_page():

    selected = option_menu(
        menu_title=None,  # required
        options=["Collection", "Action"],  # required
        default_index=0,  # optional
        orientation="horizontal",
    )
    if selected == "Collection":
        render_collection_page()
    if selected == "Action":
        render_action_page()