import pandas as pd

df = pd.read_csv("../data/raw/metrics.csv")

# ordenar
df = df.sort_values("timestamp")

# ===== FEATURES =====
df["cpu_diff"] = df["cpu"].diff()
df["ram_diff"] = df["ram"].diff()

df["cpu_ma"] = df["cpu"].rolling(5).mean()
df["cpu_std"] = df["cpu"].rolling(5).std()

# limpiar NaN
df = df.dropna()

# ===== LABEL =====
def label(row):
    if row["cpu"] > 85 and row["ram"] > 75:
        return 1
    if row["cpu_diff"] > 30:
        return 1
    if row["cpu_diff"] < -30:
        return 1
    if row["cpu_std"] > 20:
        return 1
    return 0

df["failure"] = df.apply(label, axis=1)

# guardar
df.to_csv("../data/processed/processed_metrics.csv", index=False)

print("Dataset procesado listo")
print(df["failure"].value_counts())
print(df.head())