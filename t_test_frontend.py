import streamlit as st
from modules import run_t_test_web

RUN_T_TEST = False

with st.sidebar.form(key="input_form"):

    st.info(
        "Enter a name and upload files for each group above and click 'Run Unpaired t test'",
        icon="ℹ️",
    )

    # Group 1
    st.header("**:red[Group 1 Name]**")
    group_1_name = st.text_input(
        label="**:red[Group 1 Name]**",
        placeholder="WildType",
        label_visibility="collapsed",
    )
    st.subheader("**:red[Upload files for Group 1]**")
    uploaded_files_1 = st.file_uploader(
        label="**:red[Upload files for Group 1]**",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    # Group 2
    st.header("**:blue[Group 2 Name]**")
    group_2_name = st.text_input(
        label="**:blue[Group 2 Name]**",
        placeholder="Transgenic",
        label_visibility="collapsed",
    )
    st.subheader("**:blue[Upload files for Group 2]**")
    uploaded_files_2 = st.file_uploader(
        label="**:blue[Upload files for Group 2]**",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if st.form_submit_button(label="**Run Unpaired t test**"):
        RUN_T_TEST = True

# Separate flag is needed to ensure the results are printed in the main screen
if RUN_T_TEST:
    if len(group_1_name) == 0 or len(group_2_name) == 0:
        st.error(
            "You must enter names for both groups before running the t-test!", icon="🚨"
        )
    elif len(str(uploaded_files_1)) == 0 or len(str(uploaded_files_2)) == 0:
        st.error(
            "You must upload files for both groups before running the t-test!", icon="🚨"
        )
    elif 0 > len(str(uploaded_files_1)) < 2 or 0 > len(str(uploaded_files_2)) < 2:
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
