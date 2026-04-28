import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE

# =====================================
# 1. RUTA BASE
# =====================================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "processed_metrics.csv")

print("📂 Loading dataset from:", DATA_PATH)

# =====================================
# 2. CARGA DATASET
# =====================================
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
df = df.sort_values("timestamp") # Orden temporal crítico

# =====================================
# 3. FEATURES Y TARGET
# =====================================
X = df[[
    "cpu",
    "ram",
    "disk",
    "cpu_diff",
    "ram_diff",
    "cpu_ma",
    "cpu_std"
]]

y = df["failure"]

# Limpieza de NaNs (importante para cpu_std/ma)
X = X.fillna(0)

# =====================================
# 4. SPLIT TEMPORAL MANUAL
# =====================================
# Ajustamos el split al 70% para intentar que algunas fallas queden en el test
split_index = int(len(df) * 0.7)

X_train_raw = X[:split_index]
X_test = X[split_index:]

y_train_raw = y[:split_index]
y_test = y[split_index:]

print(f"\n📊 Distribución original en entrenamiento: {y_train_raw.value_counts().to_dict()}")

# =====================================
# 5. BALANCEO CON SMOTE (Solo en entrenamiento)
# =====================================
# k_neighbors=2 porque tienes muy pocas muestras de la clase '1'
sm = SMOTE(random_state=42, k_neighbors=2)
X_train, y_train = sm.fit_resample(X_train_raw, y_train_raw)

print(f"⚖ Distribución tras SMOTE: {y_train.value_counts().to_dict()}")

# =====================================
# 6. MODELO (Configuración Robusta)
# =====================================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,            # Evita que el modelo sea demasiado específico
    min_samples_leaf=5,      # Requiere un mínimo de datos para crear una regla
    random_state=42,
    class_weight="balanced"  # Refuerzo extra para clases desequilibradas
)

# =====================================
# 7. TRAIN
# =====================================
model.fit(X_train, y_train)

# =====================================
# 8. EVALUACIÓN
# =====================================
y_pred = model.predict(X_test)

print("\n🎯 --- RESULTADOS ---")
print("Accuracy:", accuracy_score(y_test, y_pred))

# Usamos zero_division=0 para evitar warnings si el test no tiene fallas
print("\n📄 Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

print("\n🧱 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# =====================================
# 9. FEATURE IMPORTANCE
# =====================================
importance = pd.Series(model.feature_importances_, index=X.columns)
print("\n🔥 Feature importance:")
print(importance.sort_values(ascending=False))

# =====================================
# 10. GUARDAR MODELO
# =====================================
MODEL_PATH = os.path.join(BASE_DIR, "ml_service", "models", "model.pkl")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model, MODEL_PATH)

print(f"\n✔ Model saved at: {MODEL_PATH}")
print("✔ Training completed successfully")