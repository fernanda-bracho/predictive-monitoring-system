import joblib
import numpy as np
import os

# ruta robusta (NO depende de dónde ejecutes Python)
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_failure(cpu, ram, disk):
    features = np.array([[cpu, ram, disk]])
    prediction = model.predict(features)[0]

    return "FAILURE_RISK" if prediction == 1 else "NORMAL"