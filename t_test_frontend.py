""" This is the frontend script for the Unpaired, two-sample student's t test."""

import streamlit as st
from PIL import Image
from modules import run_t_test_web

RUN_T_TEST = False

st.set_page_config(layout="wide")

image = Image.open("logo.png")
st.image(image, width=300)

st.title("Unpaired, two-sample student's *t* test")

with st.form(key="input_form"):

    col1, col2 = st.columns(2)

    # Group 1
    with col1:
        st.write("**:red[Group 1 Name]**")
        group_1_name = st.text_input(
            label="**:red[Group 1 Name]**",
            label_visibility="collapsed",
        )
        st.write("**:red[Upload files for Group 1]**")
        uploaded_files_1 = st.file_uploader(
            label="**:red[Upload files for Group 1]**",
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

    # Group 2
    with col2:
        st.write("**:blue[Group 2 Name]**")
        group_2_name = st.text_input(
            label="**:blue[Group 2 Name]**",
            label_visibility="collapsed",
        )
        st.write("**:blue[Upload files for Group 2]**")
        uploaded_files_2 = st.file_uploader(
            label="**:blue[Upload files for Group 2]**",
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

    if st.form_submit_button(label="**Run Unpaired *t* test**"):
        RUN_T_TEST = True

# Separate flag is needed to ensure the results are printed in the main screen
if RUN_T_TEST:

    if len(group_1_name) == 0 or len(group_2_name) == 0:
        st.error(
            "You must enter names for both groups before running the t-test!", icon="🚨"
        )
    elif not uploaded_files_1 or not uploaded_files_2:
        st.error(
            "You must upload files for both groups before running the t-test!", icon="🚨"
        )
    else:
        # Get group data for t-tests
        group_data_for_t_test = run_t_test_web.load_files(
            group_1_name, uploaded_files_1, group_2_name, uploaded_files_2
        )

        # Perform t-tests
        run_t_test_web.perform_t_tests(
            group_data_for_t_test, group_1_name, group_2_name
        )
