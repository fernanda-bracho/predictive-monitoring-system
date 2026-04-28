import multiprocessing

def stress():
    while True:
        pass

if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    processes = []

    for _ in range(cores):
        p = multiprocessing.Process(target=stress)
        p.start()
        processes.append(p)

    print(f"Usando {cores} núcleos al 100%")