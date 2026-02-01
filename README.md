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
**Note: Linux/MacOS only support.**
1. Make sure **Docker** and **Docker Compose** are installed.
2. Download the necessary files: You only need the *docker-compose.yml* and the *.env.example* file.

3. Configure Environment Variables: Create a .env file from the example:
```bash
cp .env.example .env
```
Open .env and adjust any keys or ports if necessary.

4. Launch the application in the background:
```bash
docker-compose up -d
```
5. Access the UI: By default, the dashboard is available at [http://localhost:8501](http://localhost:8501)
6. Stop the app with
```bash
docker-compose down
```

## Testing
1. Clone this repository and go to the direcotory.
```bash
 git clone https://github.com/omoshh/edc && cd edc
```
2. Install dependencies:
```bash
 pip install -r backend/requirements.txt -r frontend/requirements.txt pytest
```
3. Run tests from the project root:
```bash
pytest test/
```
