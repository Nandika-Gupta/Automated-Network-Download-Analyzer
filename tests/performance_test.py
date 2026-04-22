import threading
import os

def run():
    os.system("python src/analyser.py")

for n in [1, 5, 10]:
    print("Testing", n)

    threads = []
    for _ in range(n):
        t = threading.Thread(target=run)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()