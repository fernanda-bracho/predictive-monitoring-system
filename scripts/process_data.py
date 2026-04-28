import pandas as pd

# leer datos reales
df = pd.read_csv("../data/metrics.csv")

# crear etiqueta (regla simple)
def label(row):
    if row["cpu"] > 80:
        return 1
    return 0

df["failure"] = df.apply(label, axis=1)

# guardar dataset listo
df.to_csv("../data/processed_metrics.csv", index=False)

print("Dataset procesado listo")
print(df.head())