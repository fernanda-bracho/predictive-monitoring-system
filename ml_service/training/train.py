import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

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

print("📊 Dataset loaded:")
print(df.head())

# =====================================
# 3. FEATURES
# =====================================
X = df[["cpu", "ram", "disk"]]
y = df["failure"]
# =====================================
# 4. SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# 5. MODEL
# =====================================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# =====================================
# 6. TRAIN
# =====================================
model.fit(X_train, y_train)

# =====================================
# 7. EVALUATION
# =====================================
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =====================================
# 8. SAVE MODEL
# =====================================
MODEL_PATH = os.path.join(BASE_DIR, "ml-service", "models", "model.pkl")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\n✔ Model saved at:", MODEL_PATH)
print("✔ Training completed successfully")