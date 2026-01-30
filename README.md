# edc

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)

edc is a system monitoring tool that displays real-time metrics through a web interface. It uses **FastAPI** to serve data, **PostgreSQL** for storage, and **Streamlit** for a reactive, user-friendly frontend.

## Features
* 📈 **Real-time Monitoring**: Track CPU, RAM, and Network usage.
* 🕒 **Historical Data**: Request metrics from specific time intervals (5m, 1h, 1d, etc.).
* 🐳 **Dockerized**: Fully containerized setup for easy deployment.
* 📊 **Interactive Charts**: Visual representations of system performance over time.

## Structure
The project approximately has the following structure:
```text
edc
├── backend
│   ├── api.py              - main API logic
│   ├── db                  
│   │   ├── database.py     - db utils for connecting and retrieving variables
│   │   ├── logger.py       - background metrics logging service 
│   │   └── setup_db.py     - initial database schema setup
│   ├── Dockerfile          - backend container definition
│   ├── requirements.txt
│   └── utils.py            - system metrics collection (psutil)
├── frontend
│   ├── main.py             - Streamlit UI and visualization
│   ├── Dockerfile          - frontend container definition
│   └── requirements.txt
├── docker-compose.yaml     - docker orchestration manifest
├── README.md
└── test                    - unit tests
    ├── api_test.py
    ├── api_validation_test.py
    ├── healthcheck.py
    ├── __init__.py
    ├── logger_test.py
    ├── setup_db_test.py
    └── utils_test.py
```
## How to use it?
**Note: Linux/MacOS only support**
1. Make sure **Docker** and **Docker Compose** are installed.
2. Clone this repository and go to the direcotory.
```bash
 git clone https://github.com/omoshh/edc && cd edc
```
4. Run with Docker Compose.
```bash
docker compose up --build
```
5. Access the UI: By default, the dashboard is available at [http://localhost:8501](http://localhost:8501)

## Testing
Run tests from the project root:
```bash
python3 -m test.healthcheck
```
Available options:
    -q, --quiet : Minimal output (only results).
    -v, --verbose : Detailed output (list of all tests).
By default, it runs with standard verbosity.
