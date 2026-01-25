# client/cli.py
import argparse
import requests

BASE_URL = "http://127.0.0.1:8000"

def set_key(key, value):
    r = requests.post(f"{BASE_URL}/set", json={"key": key, "value": value})
    print(r.json())

def get_key(key):
    r = requests.get(f"{BASE_URL}/get/{key}")
    print(r.json())

def delete_key(key):
    r = requests.delete(f"{BASE_URL}/delete/{key}")
    print(r.json())

parser = argparse.ArgumentParser(description="PyKV CLI Client")
parser.add_argument("command", choices=["set", "get", "delete"])
parser.add_argument("key")
parser.add_argument("value", nargs="?")

args = parser.parse_args()

if args.command == "set":
    set_key(args.key, args.value)
elif args.command == "get":
    get_key(args.key)
elif args.command == "delete":
    delete_key(args.key)
