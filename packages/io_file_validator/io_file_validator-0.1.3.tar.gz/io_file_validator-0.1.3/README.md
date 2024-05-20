# Welcome to IO Bytes File Validator!


[![Test](https://github.com/resilientinfrastructure/io-file-validator/actions/workflows/e2e.yml/badge.svg)](https://github.com/resilientinfrastructure/io-file-validator/actions/workflows/publish_pypi.yml)

Data Validator is your go-to tool for clean data ingestion and validation, seamlessly integrating IO Byte Files and validation tools like Panderas to make your data processing tasks a breeze.

## Features

- **Easy Data Ingestion:** Select your file format (CSV or JSON) and provide a URL to a Panderas schema.
- **Streamlined Validation:** With just a few clicks, submit your selections and validate your data effortlessly.


## io-file-validator

## Installation instructions

```sh
pip install io-file-validator
```

## Usage instructions


### Step 1: Select File Format
Choose the file format you want to ingest. Whether it's CSV or JSON, io-file-validator has got you covered.

### Step 2: Provide Panderas Schema URL
Enter the URL to the Panderas schema you want to use for validation. Don't worry, we support various schema sources to suit your needs.

Sample code:


```python

from file_validator.validator import ValidatorDataframe
validator = ValidatorDataframe(
        url="https://raw.githubusercontent.com/resilientinfrastructure/standards/main/panderas_schema.yml",
        file_format="csv",
    )
parent_path = Path(__file__).parent
sample_file_path = parent_path.resolve() / "data" / "sample_prices.csv"

with open(sample_file_path, "rb") as sample_file:
    file_contents = sample_file.read()
    sample_file_bytesio = BytesIO(file_contents)
    yaml_content = validator.get_yaml_content(validator.url)
    validated_df = validator.load_and_validate_file(my_upload=sample_file_bytesio, yaml_content=yaml_content)

```

## Run Tests
To ensure everything is functioning smoothly, run the tests using the following commands:

## Run the App
Ready to see io-file-validator in action? Simply run the following command:

## Contributions
We welcome contributions from the community! If you have any ideas, bug fixes, or enhancements, feel free to submit a pull request.

## Feedback
We'd love to hear your feedback! Whether you have suggestions for improvement or just want to share your experience using io-file-validator, don't hesitate to reach out.

Happy data ingesting with io-file-validator!

Feel free to customize it further to better suit your project's tone and style!