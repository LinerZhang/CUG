import multiprocessing
import time
import os

def cpu():
    print(f"Process {os.getpid()} started")
    while True:
        pass

if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    processes = []
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=cpu)
        p.start()
        processes.append(p)

    time.sleep(20)

    for p in processes:
        p.terminate()