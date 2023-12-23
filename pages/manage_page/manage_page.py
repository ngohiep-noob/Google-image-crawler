from streamlit_option_menu import option_menu
from pages.manage_page.collection_page import render_collection_page
from pages.manage_page.action_page import render_action_page


def manage_page():
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
