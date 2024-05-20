from abc import ABC, abstractmethod
import streamlit as st
import pandas as pd

from tempfile import NamedTemporaryFile
import streamlit as st

import pandas as pd
import pandera as pa
import requests
import yaml


class Validator():
    def __init__(self, url) -> None:
        self.url=url

    @staticmethod
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
    @staticmethod
    def read_yaml_locally(yaml_content):
        try:
            # Parse the YAML content
            yaml_data = yaml.safe_load(yaml_content)
            return yaml_data
        except yaml.YAMLError as e:
            print(f"Error reading YAML: {e}")
            return None

    def get_yaml_content(self, panderas_url):
            yaml_content = self.fetch_yaml_from_github(panderas_url)
            if yaml_content:
                # Read YAML locally
                yaml_data = self.read_yaml_locally(yaml_content)
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

    @staticmethod
    def write_dict_to_yaml(data, filename):
        try:
            with open(filename, 'w') as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)
            print(f"Dictionary successfully written to '{filename}' as YAML.")
        except IOError as e:
            print(f"Error writing YAML file: {e}")


    def validate(self, dataframe, yaml_content):
        with NamedTemporaryFile(delete=False) as ptemp:
            self.write_dict_to_yaml(yaml_content, ptemp.name)
            schema = pa.DataFrameSchema.from_yaml(ptemp.name)
            validated_df = schema.validate(dataframe)
            st.success("Validated dataframe!")
        return validated_df

    @staticmethod
    def check_size(my_upload):
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        if my_upload.size > MAX_FILE_SIZE:
            st.error(
                "The uploaded file is too large. Please upload a file smaller than 5MB."
            )

    @abstractmethod
    def read_file(self, my_upload):
        pass

    def run_validation(self, uploaded_file):
        yaml_content = self.get_yaml_content(self.url)
        dataframe=self.read_file(my_upload=uploaded_file)
        self.validate(dataframe=dataframe, yaml_content=yaml_content)


class ValidatorCsv(Validator):
    def __init__(self, url) -> None:
        super().__init__(url=url)

    def read_file(self, my_upload):
        dataframe = pd.read_csv(my_upload)
        self.check_size(my_upload=my_upload)
        return dataframe

class ValidatorJson(Validator):
    def __init__(self, url, format_type) -> None:
        super().__init__(url=url)

    def read_file(self, my_upload):
        dataframe = pd.read_json(my_upload)
        self.check_size(my_upload=my_upload)
        return dataframe
