import psutil
import time
import csv
import os

FILE_PATH = "../data/raw/metrics.csv"
machine_id = "local_pc"

# Asegurar que la carpeta existe para evitar errores de ruta
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

file_exists = os.path.exists(FILE_PATH)

print(f"Iniciando recolección persistente en: {FILE_PATH}")

# Abrimos el archivo una sola vez para mejorar la eficiencia
with open(FILE_PATH, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["timestamp", "cpu", "ram", "disk", "machine_id"])

    try:
        while True:  # Persistencia total
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Congruencia: cpu_percent(interval=1) calcula el uso real en ese segundo
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            writer.writerow([timestamp, cpu, ram, disk, machine_id])
            
            # Congruencia: Forzar escritura física al archivo para evitar pérdida de datos
            file.flush()

            print(f"{timestamp} | CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%")
            
            # No hace falta time.sleep(1) adicional porque cpu_percent(interval=1) ya espera 1s
            
    except KeyboardInterrupt:
        print("\nRecolección detenida por el usuario.")