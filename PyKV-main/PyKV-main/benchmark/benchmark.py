import time
import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000"

TOTAL_KEYS = 1000
TTL_SECONDS = 3

def random_key():
    return ''.join(random.choices(string.ascii_lowercase, k=8))


# BENCHMARK: SET WITH TTL

print("\n[1] SET Benchmark (with TTL)")
start = time.time()

keys = []
for _ in range(TOTAL_KEYS):
    key = random_key()
    keys.append(key)
    requests.post(
        f"{BASE_URL}/set",
        json={"key": key, "value": "x" * 50, "ttl": TTL_SECONDS}
    )

set_time = time.time() - start
print(f"SET {TOTAL_KEYS} keys in {set_time:.2f}s")
print(f"Throughput: {TOTAL_KEYS / set_time:.2f} ops/sec")


# BENCHMARK: GET (before expiry)

print("\n[2] GET Benchmark (before TTL expiry)")
start = time.time()

hits = 0
for key in keys:
    r = requests.get(f"{BASE_URL}/get/{key}")
    if r.status_code == 200:
        hits += 1

get_time = time.time() - start
print(f"GET hits: {hits}/{TOTAL_KEYS}")
print(f"GET time: {get_time:.2f}s")
print(f"Throughput: {TOTAL_KEYS / get_time:.2f} ops/sec")

# WAIT FOR TTL EXPIRY

print("\nWaiting for TTL expiry...")
time.sleep(TTL_SECONDS + 1)


# BENCHMARK: GET (after expiry)

print("\n[3] GET Benchmark (after TTL expiry)")
start = time.time()

misses = 0
for key in keys:
    r = requests.get(f"{BASE_URL}/get/{key}")
    if r.status_code == 404:
        misses += 1

expire_time = time.time() - start
print(f"Expired keys: {misses}/{TOTAL_KEYS}")
print(f"Post-expiry GET time: {expire_time:.2f}s")
print(f"Throughput: {TOTAL_KEYS / expire_time:.2f} ops/sec")