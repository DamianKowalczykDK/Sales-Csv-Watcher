# 📦 Sales CSV Watcher
Sales CSV Watcher is a Python-based system that monitors a directory for incoming CSV sales files,
parses and validates sales data, and generates insightful reports — now with an interactive Streamlit interface.

---
📁 Project Structure
`````
src/
├── config.py
├── file_watcher.py
├── io/
│   └── reader.py
├── model.py
├── parser.py
├── service.py
├── ui_data_service.py
├── ui_service.py
├── utils.py
tests/
├── test_config.py
├── test_file_watcher.py
├── test_model.py
├── test_parser.py
├── test_reader.py
├── test_service.py
├── test_ui_service.py
├── test_ui_data_service.py
├── test_utils.py
`````
Pipfile / Pipfile.lock  # Project dependencies

## 🚀 Getting Started
Install Pipenv (if not installed):

- pip install pipenv
Install dependencies:

- pipenv install --dev
Activate the virtual environment:

- pipenv shell

## ⚙️ Configuration (.env)

This project uses a `.env` file to configure key settings such as the watch directory, 
CSV delimiter, date and time formats, and logging.

### Example `.env` file:

- WATCH_DIR=./data

- DEFAULT_LOG_FILE=sales.log

- CSV_DELIMITER=;

- DATA_PATTERN=%Y-%m-%d

- TIME_FORMAT=%H:%M

- KEY_NAME=hour

### Notes:
- Create a `.env` file in the root directory of the project.
- Adjust the values as needed for your environment.
- The `.env` file **should NOT** be committed to version control if it contains sensitive information. 


## 🖥️ Running the Project
Backend + Watcher
Start the directory watcher and logging backend:

- pipenv run start

Streamlit Interface
Launch the interactive reporting UI:

- streamlit run main_streamlit.py

The app will be available at:

- http://localhost:8501

The app monitors the configured directory for CSV sales files, updates internal data store, and logs activity.

## 🧠 Features
✅ Watches a directory for new or updated CSV sales files

✅ Parses rows into validated Pydantic models

✅ Configurable CSV delimiters, date/time formats, and key names

✅ In-memory storage of daily and hourly grouped sales

✅ Generates reports including:

- 🧾 Daily total sales

- 📊 Average daily sales

- 📈 Sales trends (sorted)

- 🚨 Outlier detection based on standard deviation

✅ Streamlit UI:

- Report selection via sidebar

- Data tables with max value highlighting

- Optional bar or line chart toggles

- Interactive and responsive design

✅ 100% test coverage including UI logic

## 🧪 Testing
Run tests and check coverage:

- pipenv run test

Run static type checks with mypy:

- pipenv run check

## 🛠 Technologies Used

- Python 3.13.2

- Pipenv

- Streamlit

- watchdog

- Pydantic

- python-dotenv

- mypy

- pytest

- pytest-cov

- pandas

# 📬 Author
Educational project — Sales CSV Watcher

Author: Damian Kowalczyk

Year: 2025