import multiprocessing
import time

def stress_level(duration):
    start = time.time()
    while time.time() - start < duration:
        pass

if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    print(f"Iniciando estrés gradual en {cores} núcleos...")
    
    # Subir un núcleo a la vez cada 20 segundos
    for i in range(1, cores + 1):
        print(f"Activando núcleo {i}/{cores}...")
        p = multiprocessing.Process(target=stress_level, args=(60,)) # 60 seg por fase
        p.start()
        time.sleep(20) # Espera antes de subir el siguiente