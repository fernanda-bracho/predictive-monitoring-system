# Predictive Monitoring System

Sistema de monitoreo predictivo basado en microservicios que integra un backend en Java con un servicio de Machine Learning en Python.

## Arquitectura

Cliente → Spring Boot API → FastAPI ML Service → Modelo

## Tecnologías

- Java (Spring Boot)
- Python (FastAPI, scikit-learn)
- Machine Learning
- REST APIs

## Funcionalidad

El sistema analiza métricas del sistema (CPU, RAM, disco) y predice posibles fallos.

## Cómo correr el proyecto

### 1. ML Service (Python)

cd ml_service  
uvicorn app.main:app --reload  

### 2. Backend (Java)

./gradlew bootRun  

### 3. Test

POST http://localhost:8080/api/predict

{
  "cpu": 95,
  "ram": 60,
  "disk": 30
}

## Estado

Versión 1: Sistema funcional con reglas básicas y ML inicial.

## Autor
Fernanda Bracho

## ZERO TO HEROOOO
