# Predictive Monitoring System

A microservices-based predictive monitoring platform that integrates a Java Spring Boot backend with a Python (FastAPI) machine learning service to detect infrastructure anomalies before they cause failures.

## Architecture

```mermaid
graph LR
    A[Client / Postman] --> B[Spring Boot API]
    B --> C[FastAPI ML Service]
    C --> D[Random Forest Model]
```

## Tech Stack

- **Backend:** Java 17+, Spring Boot
- **ML Service:** Python 3.10+, FastAPI, Uvicorn
- **Data Science:** Scikit-learn, Pandas, NumPy (statistical analysis), imbalanced-learn (SMOTE)
- **DevOps:** Docker, Docker Compose, Git

## How It Works

The system analyzes critical infrastructure metrics (CPU, RAM, disk) and uses a Random Forest model — trained on SMOTE-balanced data — to predict potential infrastructure failures before they occur.

### Stateful Inference Engine (V2)

The ML service evolved from static predictions to a **stateful inference engine**:

- **Dynamic temporal analysis:** uses NumPy to calculate a rolling mean (`cpu_ma`) and standard deviation (`cpu_std`) in real time. The model detects instability *spikes*, not just high absolute values.
- **Per-machine persistence:** an in-memory state dictionary keeps metric history separated by `machine_id`, enabling independent monitoring of multiple servers at once.

### Dual Inference Mode

| Endpoint | Mode | Behavior |
|---|---|---|
| `POST /predict` | Real-time | Keeps machine history to detect trends and cumulative anomalies |
| `POST /predict-batch` | Forensic / historical | Processes batches in isolation (stateless), for bulk log analysis without affecting live monitoring memory |

## Running the Project

### Option A — Docker (recommended)

From the project root:

```bash
docker compose up --build
```

This builds and starts both services together:
- ML service (FastAPI) → `http://localhost:8000`
- Java service (Spring Boot) → `http://localhost:8080`

### Option B — Running services manually

**1. ML Service (Python)**
```bash
cd ml_service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**2. Backend (Java)**
```bash
cd java-service
./gradlew bootRun
```

## Testing with Postman

**Through the Java API (full end-to-end flow):**
```
POST http://localhost:8080/api/predict
```
```json
{
  "timestamp": "2026-04-28 01:00:00",
  "cpu": 95.5,
  "ram": 80.2,
  "disk": 30.0,
  "machine_id": "server_alpha"
}
```

**Directly against the ML service (single prediction):**
```
POST http://localhost:8000/predict
```
```json
{
  "timestamp": "2026-04-28 01:00:00",
  "cpu": 95.5,
  "ram": 80.2,
  "disk": 30.0,
  "machine_id": "server_alpha"
}
```

**Batch / forensic prediction:**
```
POST http://localhost:8000/predict-batch
```
```json
{
  "observations": [
    { "cpu": 10, "ram": 20, "disk": 10, "machine_id": "m1", "timestamp": "..." },
    { "cpu": 90, "ram": 85, "disk": 10, "machine_id": "m1", "timestamp": "..." }
  ]
}
```

## Author

**Fernanda Bracho**
[GitHub](https://github.com/fernanda-bracho) · [LinkedIn](https://www.linkedin.com/in/fernanda-bracho-güitron-1b9731323)
