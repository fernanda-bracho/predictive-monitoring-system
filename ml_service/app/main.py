from fastapi import FastAPI
from app.predict import predict_failure
from app.schemas import SystemData
app = FastAPI(title="Predictive Monitoring ML Service")

# Health check
@app.get("/")
def root():
    return {"message": "ML Service Running"}

# Prediction endpoint
@app.post("/predict")
def predict(data: SystemData):

    result = predict_failure(
        data.cpu,
        data.ram,
        data.disk
    )

    return {
        "prediction": result
    }