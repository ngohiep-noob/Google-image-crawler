import streamlit as st
from src.main import manager


def render_collection_page():
    location_buttons = manager.get_landmark_list()

    for location in location_buttons:
        if st.button(location):
            display_pictures(location, num_pictures=10)


def display_pictures(location, num_pictures):
    columns = st.columns(5)

    imgs = manager.images_in_landmark(location)[:num_pictures]

    for i in range(len(imgs)):
        col_index = i % 5
        shown_img = imgs[i].copy().resize((200, 200))

        columns[col_index].image(shown_img, caption=f"{location} Picture {i}")
