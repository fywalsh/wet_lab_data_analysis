""" This script does x."""

import numpy as np
import pandas as pd
import streamlit as st
import pingouin as pg


@st.cache
def load_files(group_1_name, uploaded_files_1, group_2_name, uploaded_files_2):
    """
    Loads Excel files with group data

    Args:
        group_1_name:
        uploaded_files_1:
        group_2_name:
        uploaded_files_2:

    Returns:

    """
    group_data_for_analysis = {}

    count = 0
    for file in uploaded_files_1:
        group_data_for_analysis[count] = read_data(file, group_1_name)
        count += 1

    for file in uploaded_files_2:
        group_data_for_analysis[count] = read_data(file, group_2_name)
        count += 1

    return group_data_for_analysis


def read_data(filename, group_name):
    """
    Reads group data from Excel files

    Args:
        filename:
        group_name:

    Returns:

    """
    rows_to_skip = list(range(13))
    df_data = pd.read_excel(
        filename, sheet_name="Steady-State Parameters", skiprows=rows_to_skip
    )

    # Drop 'Loop Number' column
    df_data.drop(labels="Loop Number", axis=1, inplace=True)

    # Drop last 4 rows
    df_data.drop(
        labels=range(df_data.shape[0] - 4, df_data.shape[0]), axis=0, inplace=True
    )

    # Calculate the mean value of all columns, add a row and place them in it
    df_data.loc[df_data.shape[0]] = df_data.mean()

    # Initialise a new dictionary with Group-Name and Sample-Name key/value pairs
    group_data = {"Group-Name": group_name, "Sample-Name": filename.name}

    # Add the mean values as key/value pairs for the current Group-Name and Sample-Name
    group_data.update(df_data.loc[df_data.shape[0] - 1].to_dict())

    return group_data


def perform_t_tests(group_data, group_1_name, group_2_name):
    """
    Performs t-tests

    Args:
        group_data:
        group_1_name:
        group_2_name:

    Returns:

    """
    df_group_data = pd.DataFrame.from_dict(group_data, orient="index")

    dfs = (
        run_test(df_group_data, col_name, group_1_name, group_2_name)
        for (col_name, col_value) in df_group_data.items()
    )

    st.header(group_1_name.upper() + " vs " + group_2_name.upper())

    total_df = pd.concat(dfs)
    st.dataframe(total_df)
    st.download_button(
        label="Download data as CSV",
        data=total_df.to_csv().encode("utf-8"),
        file_name=group_1_name.lower()
        + "-vs-"
        + group_2_name.lower()
        + "-unpaired-t-test-results.csv",
        mime="text/csvs",
    )


def run_test(df_group_data, col_name, group_1_name, group_2_name):
    """

    Args:
        df_group_data:
        col_name:
        group_1_name:
        group_2_name:

    Returns:

    """
    df_result = pd.DataFrame()
    if col_name != "Group-Name" and col_name != "Sample-Name":
        # Copy data for the current attribute (e.g., Heart rate (bpm)) to two separate dataframes
        # (one for each group)
        group_one = df_group_data.loc[
            df_group_data["Group-Name"] == group_1_name, col_name
        ].to_numpy()
        group_two = df_group_data.loc[
            df_group_data["Group-Name"] == group_2_name, col_name
        ].to_numpy()

        # Perform the t-test if at least one of the arrays has non-zero data
        if np.any(group_one != 0) or np.any(group_two != 0):
            # Conduct two-sample t-test
            try:
                df_result = pg.ttest(group_one, group_two, correction=False)
                df_result.insert(loc=0, column="", value=col_name)

                # Check if the p-val is significantly different
                df_result.loc[
                    df_result["p-val"] < 0.05, "Significantly Different (P < 0.05)?"
                ] = "Yes"
                df_result.loc[
                    df_result["p-val"] >= 0.05, "Significantly Different (P < 0.05)?"
                ] = "No"
            except AssertionError:
                st.error(
                    "Cannot run the t-test with the current file input, please check!",
                    icon="🚨",
                )
        else:
            # Create a blank dataframe for
            df_result = pd.DataFrame(
                data={
                    "": col_name,
                    "T": 0.0,
                    "dof": 0,
                    "alternative": "two-sided",
                    "p-val": 0.0,
                    "CI95%": "[0.0 0.0]",
                    "cohen-d": 0.0,
                    "BF10": 0.0,
                    "power": 0.0,
                    "Significantly Different (P " "< 0.05)?": "No",
                },
                index=["T-test"],
                columns=[
                    "",
                    "T",
                    "dof",
                    "alternative",
                    "p-val",
                    "CI95%",
                    "cohen-d",
                    "BF10",
                    "power",
                    "Significantly Different (P < 0.05)?",
                ],
            )

    return df_result
