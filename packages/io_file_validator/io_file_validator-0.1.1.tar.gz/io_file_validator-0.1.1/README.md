# Welcome to IO Bytes File Validator!


[![Test](https://github.com/resilientinfrastructure/file-validator/actions/workflows/e2e.yml/badge.svg)](https://github.com/resilientinfrastructure/file-validator/actions/workflows/publish_pypi.yml)

Data Validator is your go-to tool for clean data ingestion and validation, seamlessly integrating IO Byte Files and validation tools like Panderas to make your data processing tasks a breeze.

## Features

- **Easy Data Ingestion:** Select your file format (CSV or JSON) and provide a URL to a Panderas schema.
- **Streamlined Validation:** With just a few clicks, submit your selections and validate your data effortlessly.


## file-validator

## Installation instructions

```sh
pip install file-validator
```

## Usage instructions

```python

from file_validator.validator import ValidatorDataframe

validated_df = run_validate_file()

st.write(validated_df)
```


## Instructions

### Step 1: Select File Format
Choose the file format you want to ingest. Whether it's CSV or JSON, file-validator has got you covered.

### Step 2: Provide Panderas Schema URL
Enter the URL to the Panderas schema you want to use for validation. Don't worry, we support various schema sources to suit your needs.


[Go to Demo](https://youtu.be/9Ry_A9LgrbQ)

[![Video](http://img.youtube.com/vi/9Ry_A9LgrbQ/0.jpg)](https://youtu.be/9Ry_A9LgrbQ)


## Run Tests
To ensure everything is functioning smoothly, run the tests using the following commands:

## Run the App
Ready to see file-validator in action? Simply run the following command:



## Contributions
We welcome contributions from the community! If you have any ideas, bug fixes, or enhancements, feel free to submit a pull request.

## Feedback
We'd love to hear your feedback! Whether you have suggestions for improvement or just want to share your experience using file-validator, don't hesitate to reach out.

Happy data ingesting with file-validator!

Feel free to customize it further to better suit your project's tone and style!