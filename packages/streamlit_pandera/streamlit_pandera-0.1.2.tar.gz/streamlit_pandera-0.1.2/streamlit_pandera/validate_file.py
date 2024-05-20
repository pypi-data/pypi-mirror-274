import logging
from tempfile import NamedTemporaryFile

import pandas as pd
import pandera as pa
import requests
import streamlit as st
import validators
import yaml
from io_file_validator.validator import ValidatorDataframe

logger = logging.getLogger(__name__)
if "file_format" not in st.session_state:
    st.session_state["file_format"] = "Unassigned"

if "file_format" not in st.session_state:
    st.session_state["panderas_url"] = "Unassigned"


def assign_file_format(file_format):
    st.session_state["file_format"] = file_format


def assing_panderas_url(panderas_url):
    if validators.url(panderas_url):
        st.success("Valid URL! Proceed.")
    st.session_state["panderas_url"] = panderas_url


def set_selectbox(supported_files):
    selectbox = st.selectbox(
        label="File format (default is csv)",
        options=(supported_files),
    )
    assign_file_format(selectbox)


def set_format_type_form():
    with st.form(key="my_form"):
        panderas_url = st.text_input(label="Enter Panderas Yaml URL")
        damn = st.form_submit_button(label="Submit", on_click=assing_panderas_url(panderas_url))
        if damn:
            try:
                if st.session_state["file_format"] == "Unassigned":
                    st.session_state["file_format"] = "csv"
                return
            except:
                st.error("Invalid URL! Please enter a valid URL.")
                return


def run_validate_file(
    validator: ValidatorDataframe = ValidatorDataframe(url=None, file_format=None),
    additional_supported_files: list = None,
):
    st.set_page_config(
        page_title="Data Validator Home",
        page_icon="📊",
    )
    supported_files = ["csv", "json"]
    if additional_supported_files and isinstance(additional_supported_files, list):
        supported_files.extend(additional_supported_files)

    st.write("# Data Validation Tool! 📊")
    set_selectbox(supported_files)
    set_format_type_form()
    if st.session_state["panderas_url"] is not None and st.session_state["file_format"] is not None:
        if st.session_state["file_format"] == "csv":
            validator.url = st.session_state["panderas_url"]
            validator.file_format = st.session_state["file_format"]
        elif st.session_state["file_format"] == "json":
            validator.url = st.session_state["panderas_url"]
            validator.file_format = st.session_state["file_format"]
        else:
            raise Exception(f"File Format {st.session_state['file_format']} Not Selected or Supported")

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            dataframe = validator.run_validation(uploaded_file=uploaded_file)
            st.success("Validated dataframe!")
            st.dataframe(dataframe)
            st.balloons()
            return uploaded_file
