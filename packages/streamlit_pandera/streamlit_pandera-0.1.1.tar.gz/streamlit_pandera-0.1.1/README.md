# Welcome to Streamlit-Panderas!


[![Test](https://github.com/resilientinfrastructure/streamlit-panderas/actions/workflows/e2e.yml/badge.svg)](https://github.com/resilientinfrastructure/streamlit-panderas/actions/workflows/e2e.yml)

Streamlit-Panderas is your go-to tool for clean data ingestion and validation, seamlessly integrating Streamlit and Panderas to make your data processing tasks a breeze.

## Features

- **Easy Data Ingestion:** Select your file format (CSV or JSON) and provide a URL to a Panderas schema.
- **Streamlined Validation:** With just a few clicks, submit your selections and validate your data effortlessly.


## streamlit-panderas

## Installation instructions

```sh
pip install streamlit-panderas
```

## Usage instructions

```python
import streamlit as st

from streamlit_pandera.validate_file  import run_validate_file

validated_df = run_validate_file()

st.write(validated_df)
```


## Instructions

### Step 1: Select File Format
Choose the file format you want to ingest. Whether it's CSV or JSON, Streamlit-Panderas has got you covered.

### Step 2: Provide Panderas Schema URL
Enter the URL to the Panderas schema you want to use for validation. Don't worry, we support various schema sources to suit your needs.

### Step 3: Submit and Validate
Hit that submit button and let Streamlit-Panderas work its magic! Your data will be validated against the specified schema in no time.


[Go to Demo](https://youtu.be/9Ry_A9LgrbQ)

[![Video](http://img.youtube.com/vi/9Ry_A9LgrbQ/0.jpg)](https://youtu.be/9Ry_A9LgrbQ)


## Run Tests
To ensure everything is functioning smoothly, run the tests using the following commands:

```bash
poetry install
poetry run playwright install
poetry run pytest e2e
```

## Run the App
Ready to see Streamlit-Panderas in action? Simply run the following command:

```bash
poetry run streamlit run streamlit_panderas/validate_file.py
```

## Contributions
We welcome contributions from the community! If you have any ideas, bug fixes, or enhancements, feel free to submit a pull request.

## Feedback
We'd love to hear your feedback! Whether you have suggestions for improvement or just want to share your experience using Streamlit-Panderas, don't hesitate to reach out.

Happy data ingesting with Streamlit-Panderas!

Feel free to customize it further to better suit your project's tone and style!