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
* ☸️ **Kubernetes-ready**: Manifests included for cluster deployment.
* 📊 **Interactive Charts**: Visual representations of system performance over time.

## Architecture
```text
Streamlit UI  ──HTTP──▶  FastAPI  ──SQL──▶  PostgreSQL
  (:8501)                (:8000)             (:5432)
```
A background logger runs inside the backend, sampling host metrics every 30s (via `psutil` reading the mounted `/proc`) and writing them to the database. The API serves the latest sample and historical ranges to the frontend.

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
├── k8s                     - Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── db.yaml
│   └── frontend-deployment.yaml
├── docker-compose.yaml     - docker orchestration manifest
├── README.md
└── test                    - unit tests
    ├── api_test.py
    ├── api_validation_test.py
    ├── __init__.py
    ├── logger_test.py
    ├── setup_db_test.py
    └── utils_test.py
```

## API
The backend exposes two endpoints (interactive docs at `http://localhost:8000/docs`):

| Method | Path | Query params | Description |
|--------|------|--------------|-------------|
| `GET` | `/metrics` | — | Returns the most recent metric sample. |
| `GET` | `/metrics/range` | `start`, `end` (ISO 8601 timestamps) | Returns all samples between `start` and `end`. |

Each metric contains: `timestamp`, `cpu_usage`, `ram_usage`, `load_average`, `network_bandwidth`.

## Configuration
Copy `.env.example` to `.env` and adjust as needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_NAME` | `db_metrics` | Application database name. |
| `DB_USER` | `postgres` | Database user. |
| `DB_PASS` | — | Database password. |
| `DB_HOST` | `db` | Database host (service name in Docker/K8s). |
| `DB_PORT` | `5432` | Database port. |
| `DB_TABLE` | `metrics_db` | Table holding metric samples. |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | — | Credentials consumed by the Postgres container. Keep in sync with `DB_*`. |
| `API_HOST` | `0.0.0.0` | Address the API binds to. |
| `API_PORT` | `8000` | API port. |
| `API_METRICS` | `http://backend:8000/metrics` | Latest-metric URL used by the frontend. |
| `API_RANGE` | `http://backend:8000/metrics/range` | Range URL used by the frontend. |
| `APP_PORT` | `8501` | Streamlit UI port. |
| `APP_ADDRESS` | `0.0.0.0` | Address the UI binds to. |

## How to use it? (Docker Compose)
**Note: Linux host required** — the backend mounts the host `/proc` in privileged mode to read real metrics, which is not available on the macOS/Windows Docker VM.
1. Make sure **Docker** and **Docker Compose** are installed.
2. Download the necessary files: you only need `docker-compose.yaml` and `.env.example`.
3. Configure environment variables. Create a `.env` file from the example:
```bash
cp .env.example .env
```
Open `.env` and adjust any keys or ports if necessary.
4. Launch the application in the background:
```bash
docker-compose up -d
```
5. Access the UI: by default, the dashboard is available at [http://localhost:8501](http://localhost:8501).
6. Stop the app with:
```bash
docker-compose down
```

## Kubernetes
Manifests in `k8s/` deploy the same stack to a cluster: backend (`Deployment` + `ClusterIP` service), Postgres (`Deployment` + `PersistentVolumeClaim` + service), and frontend (`Deployment` + `LoadBalancer` service).

1. The manifests read environment variables from a `ConfigMap` named `edc-config`. Create it from your `.env` first:
```bash
kubectl create configmap edc-config --from-env-file=.env
```
2. Apply the manifests:
```bash
kubectl apply -f k8s/
```
> **Notes:**
> - The backend requires `privileged: true` and a `hostPath` mount of `/proc` to collect metrics.
> - Manifests use the namespace `ammonia-edc-edc-test` and a `kube-dc` HTTPS annotation on the frontend service — adjust these to match your cluster.

## Testing
1. Clone this repository and go to the directory:
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
