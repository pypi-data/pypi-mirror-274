from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile

import pandas as pd
import pandera as pa
import requests
import yaml


class Validator:
    def __init__(self, file_format) -> None:
        self.file_format = file_format

    @staticmethod
    def check_size(my_upload):
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        if my_upload.size > MAX_FILE_SIZE:
            print("The uploaded file is too large. Please upload a file smaller than 5MB.")

    @abstractmethod
    def load_and_validate_file(self, my_upload, yaml_content):
        pass

    @abstractmethod
    def run_validation(self, uploaded_file):
        pass


class ValidatorDataframe(Validator):
    def __init__(self, url, file_format) -> None:
        super().__init__(file_format=file_format)
        self._validation_method = "yaml_url"
        self.url = url

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
            with open(filename, "w") as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)
            print(f"Dictionary successfully written to '{filename}' as YAML.")
        except IOError as e:
            print(f"Error writing YAML file: {e}")

    def load_and_validate_file(self, my_upload, yaml_content):
        dataframe = self.read_file(my_upload=my_upload)
        validated_df = self.validate_file(dataframe=dataframe, yaml_content=yaml_content)
        return validated_df

    def validate_file(self, dataframe, yaml_content):
        with NamedTemporaryFile(delete=False) as ptemp:
            standard_yaml_file_name = ptemp.name
            self.write_dict_to_yaml(yaml_content, standard_yaml_file_name)
            validated_df = self.validate(dataframe=dataframe, file_name=standard_yaml_file_name)
            st.success("Validated dataframe!")
        return validated_df

    def read_file(self, my_upload):
        if self.file_format == "json":
            dataframe = pd.read_json(my_upload)
        elif self.file_format == "csv":
            dataframe = pd.read_csv(my_upload)

        return dataframe

    def validate(self, dataframe, file_name):
        schema = pa.DataFrameSchema.from_yaml(file_name)
        validated_df = schema.validate(dataframe)
        return validated_df

    def run_validation(self, uploaded_file) -> pd.DataFrame:
        if self._validation_method == "yaml_url":
            self.check_size(my_upload=uploaded_file)
            yaml_content = self.get_yaml_content(self.url)
            validated_df = self.load_and_validate_file(my_upload=uploaded_file, yaml_content=yaml_content)
        return validated_df
