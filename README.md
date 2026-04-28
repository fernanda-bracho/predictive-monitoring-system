Predictive Monitoring System
Sistema de monitoreo predictivo basado en microservicios que integra un backend en Java Spring Boot con un servicio de Machine Learning en Python (FastAPI).

Arquitectura
Fragmento de código
graph LR
  A[Cliente/Postman] --> B[Spring Boot API]
  B --> C[FastAPI ML Service]
  C --> D[Random Forest Model]
  
Tecnologías
Backend: Java 17+, Spring Boot
ML Service: Python 3.10+, FastAPI, Uvicorn
Data Science: Scikit-learn, Pandas, Numpy (Análisis estadístico)
DevOps: Docker, Docker Compose, Git  - - En esta version aun no esta disponible esto

Funcionalidad
El sistema analiza métricas críticas (CPU, RAM, disco) y utiliza un modelo de Random Forest entrenado con datos balanceados (SMOTE) para predecir posibles fallos de infraestructura antes de que ocurran.

Actualización: Motor de Inferencia con Memoria (V2)
He evolucionado el servicio de Machine Learning de una predicción estática a un Motor de Inferencia de Estado (Stateful).

Cambios Clave:
Análisis Temporal Dinámico: Integración de numpy para calcular la media móvil (cpu_ma) y la desviación estándar (cpu_std) en tiempo real. El modelo ahora detecta "picos" de inestabilidad, no solo valores altos.

Persistencia por Máquina: Implementación de un diccionario de estados que separa el historial de métricas por machine_id, permitiendo el monitoreo independiente de múltiples servidores.

Dual Inference Mode:

POST /predict: Modo Real-time. Mantiene el historial de la máquina para detectar tendencias y anomalías acumulativas.

POST /predict-batch: Modo Forense/Histórico. Procesa lotes de datos de forma aislada (Stateless) para análisis masivo de logs sin contaminar la memoria del monitoreo en vivo.

Cómo correr el proyecto
1. ML Service (Python)
Bash
cd ml_service
pip install -r requirements.txt
uvicorn app.main:app --reload
2. Backend (Java)
Bash
cd java-service
./gradlew bootRun
3. Pruebas (Postman)
Predicción Simple:
POST http://localhost:8000/predict

JSON
{
  "timestamp": "2026-04-28 01:00:00",
  "cpu": 95.5,
  "ram": 80.2,
  "disk": 30.0,
  "machine_id": "server_alpha"
}
Predicción en Batch:
POST http://localhost:8000/predict-batch

JSON
{
  "observations": [
    { "cpu": 10, "ram": 20, "disk": 10, "machine_id": "m1", "timestamp": "..." },
    { "cpu": 90, "ram": 85, "disk": 10, "machine_id": "m1", "timestamp": "..." }
  ]
}
 Autor
Fernanda Bracho 

## ZERO TO HEROOOO 
