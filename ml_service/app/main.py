from fastapi import FastAPI
from app.predict import predict_failure, state  # <--- IMPORTAMOS 'state'
from app.schemas import SystemData, SystemDataBatch

app = FastAPI(title="Predictive Monitoring ML Service")

@app.get("/")
def root():
    return {"message": "ML Service Running"}

@app.post("/predict")
def predict(data: SystemData):
    return {"prediction": predict_failure(data.cpu, data.ram, data.disk, data.machine_id)}



@app.post("/predict-batch")
def predict_batch(batch: SystemDataBatch):
    results = []
    
    # 🔥 EL TRUCO: Limpiamos el historial global antes de procesar el lote
    # Esto evita que el dato 1 influya en el dato 2 dentro del mismo Batch.
    state.clear() 

    for item in batch.observations:
        result = predict_failure(
            item.cpu,
            item.ram,
            item.disk,
            item.machine_id
        )
        results.append(result)
        
    return {"predictions": results}