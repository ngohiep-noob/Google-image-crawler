import streamlit as st

def render_collection_page():
    location_buttons = ['Hoi An', 'Ha Long Bay', 'Hoan Kiem Lake', 'Vung Tau']

    for location in location_buttons:
        if st.button(location):
            display_pictures(location, num_pictures=10)

def display_pictures(location, num_pictures):
    columns = st.columns(5)

    for i in range(1, num_pictures + 1):
        image_path = f"cau hien luong\\1.jpg" # Adjust the filename pattern as needed
        col_index = (i - 1) % 5
        columns[col_index].image(image_path, caption=f'{location} Picture {i}', width=200)