#!/usr/bin/env python

# Built-in Libraries
import argparse
import glob
import os
import time
import warnings

# External Libraries
import numpy as np
import pandas as pd
import pingouin as pg

warnings.simplefilter("error", RuntimeWarning)


def load_files(groups):
    """
    Loads Excel files with group data

    Args:
        groups:

    Returns:

    """
    group_data_for_analysis = {}

    count = 0
    for group in groups.split(","):
        for file in glob.glob(os.path.join(args.input_dir + "\\" + group, "*.xlsx")):
            print(f"Reading Excel File: {file}")
            group_data_for_analysis[count] = read_data(file, group)
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
    group_data = {
        "Group-Name": group_name,
        "Sample-Name": filename[filename.rfind("\\") + 1 : -4],
    }

    # Add the mean values as key/value pairs for the current Group-Name and Sample-Name
    group_data.update(df_data.loc[df_data.shape[0] - 1].to_dict())

    return group_data


def perform_t_tests(group_data, group_names):
    """
    Performs t-tests

    Args:
        group_data:
        group_names:

    Returns:

    """
    df_group_data = pd.DataFrame.from_dict(group_data, orient="index")

    print("Running T-Tests......")

    start_row = 0
    current_date_time = time.strftime("%d%m%Y_%H%M")
    for col_name in df_group_data.iteritems():
        if col_name != "Group-Name" and col_name != "Sample-Name":
            # Copy data for the current attribute (e.g., Heart rate (bpm)) to two separate dataframes (one for each
            # group)
            group_one = df_group_data.loc[
                df_group_data["Group-Name"] == group_names.split(",")[0], col_name
            ].to_numpy()
            group_two = df_group_data.loc[
                df_group_data["Group-Name"] == group_names.split(",")[1], col_name
            ].to_numpy()

            # Perform the t-test if at least one of the arrays has non-zero data
            if np.any(group_one != 0) or np.any(group_two != 0):
                # Conduct two-sample t-test
                df_result = pg.ttest(group_one, group_two, correction=False)  # type: ignore
                df_result.insert(loc=0, column="", value=col_name)

                # Check if the p-val is significantly different
                df_result.loc[
                    df_result["p-val"] < 0.05, "Significantly Different (P < 0.05)?"
                ] = "Yes"
                df_result.loc[
                    df_result["p-val"] >= 0.05, "Significantly Different (P < 0.05)?"
                ] = "No"
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

            # Print the result to Excel
            results_file = (
                args.input_dir
                + "\\"
                + group_names.split(",")[0]
                + "_vs_"
                + group_names.split(",")[1]
                + "_"
                + current_date_time
                + ".xlsx"
            )
            if os.path.exists(results_file):
                open_mode = "a"
            else:
                open_mode = "w"

            with pd.ExcelWriter(
                results_file,
                mode=open_mode,
                engine="openpyxl",
                if_sheet_exists="overlay",
            ) as writer:
                df_result.to_excel(writer, sheet_name="Sheet1", startrow=start_row)

            start_row += 2

    print(f"T-Test results saved to {results_file}")


if __name__ == "__main__":
    print(f"Running Script: {__file__}")

    parser = argparse.ArgumentParser(
        prog=__file__, usage="%(prog)s [options]", description="Performs Data Analysis"
    )

    # -i input_dir -g group_list
    parser.add_argument("-i", "--input_dir", help="Input directory")
    parser.add_argument("-g", "--group_list", help="Comma separated list of groups")

    args = parser.parse_args()

    # Get group data for t-tests
    group_data_for_t_test = load_files(args.group_list)

    # Perform t-tests
    perform_t_tests(group_data_for_t_test, args.group_list)
