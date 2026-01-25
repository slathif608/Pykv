import json
import os
from core.ttl_heap import TTLHeap as ttl

LOG_FILE = "data/pykv.log"
COMPACTED_LOG_FILE = "data/pykv_compacted.log"

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")


def append_log(operation: str, key: str, value=None, ttl=None):
    entry = {
        "op": operation,
        "key": key,
        "value": value,
        "ttl":ttl
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    if os.path.getsize(LOG_FILE) > 10 * 1024 * 1024:  # 10MB
        compact_log()



def recover_store(store):
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        for line in f:
            entry = json.loads(line)

            if entry["op"] == "SET":
                key = entry["key"]
                value = entry["value"]
                ttl = entry["ttl"]
                store.set(key, value, ttl)
            elif entry["op"] == "DELETE":
                store.delete(entry["key"])

    os.remove(LOG_FILE)

def compact_log():
    latest_state = {}

    # Step 1: Read existing log
    with open(LOG_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            op = parts[0]
            key = parts[1]

            if op == "SET":
                value = parts[2]
                latest_state[key] = ("SET", value)
            elif op == "DELETE":
                latest_state[key] = ("DELETE", None)

    # Step 2: Write compacted log
    with open(COMPACTED_LOG_FILE, "w") as f:
        for key, (op, value) in latest_state.items():
            if op == "SET":
                f.write(f"SET,{key},{value}\n")
            else:
                f.write(f"DELETE,{key}\n")

    # Step 3: Atomic replace
    os.replace(COMPACTED_LOG_FILE, LOG_FILE)
def compact_log(store, log_file="pykv.log"):
    temp_file = "pykv.compact.log"

    with open(temp_file, "w") as f:
        for key in store.keys():
            value = store.get(key)
            f.write(f"SET {key} {value}\n")

    os.replace(temp_file, log_file)
