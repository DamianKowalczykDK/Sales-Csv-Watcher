# 📦 Sales CSV Watcher
A Python-based system to watch a directory for sales CSV files, parse and validate sales data, and generate reports in real time.

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
├── utils.py
tests/
├── test_config.py
├── test_file_watcher.py
├── test_model.py
├── test_parser.py
├── test_reader.py
├── test_service.py
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
Start the watcher and sales service by running:

- pipenv run start

The app monitors the configured directory for CSV sales files, updates internal data store, and logs activity.

## 🧠 Features
✅ Watches directories for new, modified, or deleted CSV files using watchdog.

✅ Parses CSV rows into validated Pydantic models.

✅ Supports configurable CSV delimiters, date/time formats, and key names via .env file.

✅ Stores sales data grouped by date and hour in memory.

✅ Provides a simple service layer to generate sales reports.

✅ Logs all key events and errors for traceability.

## 🧪 Testing
Run tests and check coverage:

- pipenv run test

Run static type checks with mypy:

- pipenv run check

## 🛠 Technologies Used
Python 3.13.2

- Pipenv

- watchdog

- pydantic

- python-dotenv

- mypy

- pytest

- pytest-cov

📬 Author
Educational project — Sales CSV Watcher

Author: Damian Kowalczyk
Year: 2025