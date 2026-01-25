import time
import threading
import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000"
SECONDARY_URL = "http://127.0.0.1:8001"
THREADS = 10
OPS_PER_THREAD = 100
written_keys = []
lock = threading.Lock()

def random_key():
    return ''.join(random.choices(string.ascii_letters, k=8))

def worker():
    for _ in range(OPS_PER_THREAD):
        key = random_key()
        requests.post(
            f"{BASE_URL}/set",
            json={"key": key, "value": "123"}
        )

        with lock:
            written_keys.append(key)


def verify_replication():
    failures = 0

    for key in written_keys[:50]:  # sample
        r = requests.get(f"{SECONDARY_URL}/get/{key}")
        if r.status_code != 200:
            failures += 1

    print(f"Replication failures: {failures}")

threads = []
start = time.time()

for _ in range(THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end = time.time()

total_ops = THREADS * OPS_PER_THREAD * 2
print(f"Total ops: {total_ops}")
print(f"Time taken: {end - start:.2f}s")
print(f"Throughput: {total_ops / (end - start):.2f} ops/sec")
