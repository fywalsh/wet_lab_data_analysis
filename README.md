# Automated *t* test calculation tool for Pressure-Volume Loop (PVL) data #

Python tool to perform an unpaired, two-sample student's *t* test on the mean values of Pressure-Volume Loop measurements (e.g., Heart rate (bpm), End-diastolic Volume (µL), Cardiac Output (µL/min)) for two groups (e.g., WildType vs Transgenic).  Note: this tool has been designed to ingest Excel files with a specific format produced by a specific wet lab software (i.e., PVAN Ultra).  See [here](test_files/) for examples of the input files.  

___

## Installation (*Command Line Tool Only*)

Use the package manager <a href="https://pip.pypa.io/en/stable/" target="_blank">pip</a> to install requirements.txt.

```bash
pip install -r requirements.txt
```
___

## Usage

The tool can be run as a web application (already deployed on the **Streamlit Platform**) or via the Command Line.

### Web Application
To use the web application, click  <a href="https://fywalsh-wet-lab-data-analysis-t-test-frontend-ngpzd4.streamlit.app/" target="_blank"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>  and perform the following:
* Type a group name (e.g., WildType) for Group 1.
* Upload all files for Group 1 (e.g., [WT#1.xlsx](test_files/WT%231.xlsx), [WT#2.xlsx](test_files/WT%232.xlsx), [WT#3.xlsx](test_files/WT%233.xlsx)) for Group 1.
* Type a group name (e.g., Transgenic) for Group 2.
* Upload all files for Group 2 (e.g., [TG#1.xlsx](test_files/TG%231.xlsx), [TG#2.xlsx](test_files/TG%231.xlsx), [TG#3.xlsx](test_files/TG%233.xlsx)) for Group 2.
* Click **Run Unpaired *t* test**.
	* A bar chart comparing the *p-val* for each measurement will appear, to expand it hover over it and a set of arrows will appear on the right - click to expand.  Click on the same arrows to return to the original view.
	* A table showing raw results from the test will also appear (expand in the same manner as above).  These results can be download as a CSV by clicking on the download button.  *Note: that clicking on the button will cause the results to disappear from screen - this is due to Streamlit rerunning the whole application when it receives any input - click on **Run Unpaired *t* test** to reload the results.*

### Command Line Tool
To use the command line tool, perform the following:
* Create a folder for each group and store the relevant Excel files in each one, for example:
	```cmd
	C:\data
	+---Transgenic
	|		TG#1.xlsx
	|		TG#2.xlsx
	|		TG#3.xlsx
	+---WildType
	|		WT#1.xlsx
	|		WT#2.xlsx
	|		WT#3.xlsx
	```
* Run the following command (on the command line):
	```bash
	python run_t_test_cmd.py -i <input_dir> -o <output_dir> -g <group1,group2>
	```
	**Example:** 
	```bash
	python run_t_test_cmd.py -i C:\data -o C:\results -g Transgenic,WildType
	```
* The results will be saved to an Excel file named *Group1_vs_Group2_DDMMYYYY_HHMI.xlsx* in the output directory.