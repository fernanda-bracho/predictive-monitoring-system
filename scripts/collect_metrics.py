import psutil
import time
import csv

with open("metrics.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["cpu", "ram", "disk"])

    for _ in range(60):  # 60 segundos de datos
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        print(f"CPU: {cpu} | RAM: {ram} | Disk: {disk}")

        writer.writerow([cpu, ram, disk])
        time.sleep(1)
        print(df["failure"].value_counts())

print("Datos recolectados")
