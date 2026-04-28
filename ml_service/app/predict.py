import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "model.pkl"
)

model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=4,       # <--- IMPORTANTE: No dejes que el árbol sea muy profundo
    min_samples_leaf=5, # <--- IMPORTANTE: Evita que aprenda de filas aisladas
    random_state=42
)

model = joblib.load(MODEL_PATH)

# memoria por máquina
state = {}

def predict_failure(cpu, ram, disk, machine_id="default"):
    global state

    # inicializar si no existe
    if machine_id not in state:
        state[machine_id] = {
            "last_cpu": None,
            "last_ram": None,
            "history_cpu": []
        }

    machine = state[machine_id]

    # ===== DIFF =====
    if machine["last_cpu"] is None:
        cpu_diff = 0
        ram_diff = 0
    else:
        cpu_diff = cpu - machine["last_cpu"]
        ram_diff = ram - machine["last_ram"]

    # ===== HISTORIAL =====
    machine["history_cpu"].append(cpu)
    if len(machine["history_cpu"]) > 5:
        machine["history_cpu"].pop(0)

    # ===== STATS =====
    cpu_ma = np.mean(machine["history_cpu"])
    cpu_std = np.std(machine["history_cpu"])

    # guardar estado
    machine["last_cpu"] = cpu
    machine["last_ram"] = ram

    # ===== FEATURES =====
    features = np.array([[
        cpu,
        ram,
        disk,
        cpu_diff,
        ram_diff,
        cpu_ma,
        cpu_std
    ]])

    prediction = model.predict(features)[0]

    return "FAILURE_RISK" if prediction == 1 else "NORMAL"