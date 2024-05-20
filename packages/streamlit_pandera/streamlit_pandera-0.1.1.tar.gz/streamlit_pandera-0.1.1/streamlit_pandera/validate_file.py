import streamlit as st
import pandas as pd

from tempfile import NamedTemporaryFile
import streamlit as st
import logging

import pandas as pd
import validators
import pandera as pa
import requests
import yaml
from streamlit_pandera.validator import ValidatorCsv, ValidatorJson

logger = logging.getLogger(__name__)
if "file_format" not in st.session_state:
    st.session_state["file_format"] = "Unassigned"

if "file_format" not in st.session_state:
    st.session_state["panderas_url"] = "Unassigned"


def fetch_yaml_from_github(url):
    try:
        # Send a GET request to fetch the raw content of the YAML file from GitHub
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        yaml_content = response.text
        return yaml_content
    except requests.RequestException as e:
        print(f"Error fetching YAML from GitHub: {e}")
        return None

def read_yaml_locally(yaml_content):
    try:
        # Parse the YAML content
        yaml_data = yaml.safe_load(yaml_content)
        return yaml_data
    except yaml.YAMLError as e:
        print(f"Error reading YAML: {e}")
        return None

def get_yaml_content(panderas_url):
        yaml_content = fetch_yaml_from_github(panderas_url)
        if yaml_content:
            # Read YAML locally
            yaml_data = read_yaml_locally(yaml_content)
            if yaml_data:
                print("YAML file fetched and read successfully:")
                print(yaml_data)
                return yaml_data
            else:
                print("Failed to read YAML locally.")
                return None
        else:
            print("Failed to fetch YAML from GitHub.")
            return None

def assign_file_format(file_format):
    st.session_state["file_format"] = file_format

def assing_panderas_url(panderas_url):
    if validators.url(panderas_url):
        st.success("Valid URL! Proceed.")
    st.session_state["panderas_url"] = panderas_url

def write_dict_to_yaml(data, filename):
    try:
        with open(filename, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
        print(f"Dictionary successfully written to '{filename}' as YAML.")
    except IOError as e:
        print(f"Error writing YAML file: {e}")

def validate(dataframe, yaml_content):
    with NamedTemporaryFile(delete=False) as ptemp:
        write_dict_to_yaml(yaml_content, ptemp.name)
        schema = pa.DataFrameSchema.from_yaml(ptemp.name)
        validated_df = schema.validate(dataframe)
        st.success("Validated dataframe!")
    return validated_df


def set_selectbox():
    selectbox = st.selectbox(
        label='File format (default is csv)',
        options=(['csv', 'json']),
    )
    assign_file_format(selectbox)

def set_format_type_form():
    with st.form(key='my_form'):
        panderas_url = st.text_input(label='Enter Panderas Yaml URL')
        damn = st.form_submit_button(label='Submit', on_click=assing_panderas_url(panderas_url))
        if damn:
            try:
                if st.session_state["file_format"] == "Unassigned":
                    st.session_state["file_format"] = "csv"
                return
            except:
                st.error("Invalid URL! Please enter a valid URL.")
                return

def run_validate_file():
    st.set_page_config(
        page_title="Clean Data Home",
        page_icon="📊",
    )
    st.write("# Clean Data Validation Tool! 📊")
    set_selectbox()
    set_format_type_form()
    if st.session_state["panderas_url"] is not None:
        if st.session_state["file_format"] == "csv":
            validator = ValidatorCsv(url=st.session_state["panderas_url"])
        if st.session_state["file_format"] == "json":
            validator = ValidatorJson(url=st.session_state["panderas_url"])

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            dataframe = validator.run_validation(uploaded_file=uploaded_file)
            st.dataframe(dataframe)
            st.balloons()
            return uploaded_file


