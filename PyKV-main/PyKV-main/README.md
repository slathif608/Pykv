📦 PyKV — A Scalable In‑Memory Key‑Value Store with Persistence
<p align="center"> <img src="assets/pykv-banner.png" alt="PyKV Banner" width="800"/> </p> <p align="center"> <b>High‑performance, persistent, and observable in‑memory key‑value store</b><br> Inspired by Redis • Built with FastAPI • Designed for systems engineering learning </p>
🚀 Project Overview
PyKV is a production‑inspired, in‑memory key‑value store designed to demonstrate systems design fundamentals such as:

Low‑latency data access

LRU cache eviction

Write‑Ahead Logging (WAL)

TTL‑based expiration

Metrics & observability

Session‑based authentication

Primary‑Secondary replication (foundation)

This project is not just CRUD — it simulates how real systems like Redis and Memcached are built internally.

✨ Key Features
🔹 Core Storage Engine
O(1) GET / SET / DELETE operations

Custom LRU cache using doubly‑linked list

Capacity‑based eviction

🔹 Persistence (Durability)
Append‑only Write‑Ahead Log (WAL)

Crash recovery from logs

Manual log compaction

🔹 TTL (Time‑To‑Live)
Per‑key expiration

Lazy + background cleanup

TTL countdown API

🔹 Observability & Stats
Total operations count

Cache evictions

TTL expirations

Store uptime

WAL file size

🔹 Authentication & Sessions
Register / Login

Session‑based auth using cookies

“Remember Me” support

🔹 UI Dashboard
Browser‑based frontend

Dark mode

TTL input

Stats dashboard

Responsive design

🔹 Replication (Foundation)
Primary → Secondary model

Write forwarding to secondary

Environment‑based role switching

🧠 System Architecture

<p align="center"> <img src="assets/architecture.png" alt="Architecture Diagram" width="700"/> </p>

Client (Browser / CLI)

        |
        v
        
FastAPI API Layer

        |
        v
        
In‑Memory Store (LRU + TTL)

        |
        v
        
Write‑Ahead Log (Persistence)

        |
        v
        
Secondary Node (Replication)


🗂️ Project Structure

PyKV/

├── main.py               # FastAPI app & routes

├── store.py              # LRU + TTL + stats

├── persistence.py        # WAL & recovery

├── auth.py               # User auth

├── data/

│   ├── users.json

│   └── pykv.log

├── templates/

│   ├── login.html

│   ├── register.html

│   ├── dashboard.html

│   └── stats.html

├── static/

│   ├── css/style.css

│   └── js/app.js

├── benchmark/

│   └── benchmark.py

├── assets/

│   ├── pykv-banner.png

│   ├── architecture.png

│   └── stats-ui.png

└── README.md

⚙️ Tech Stack

Layer	Technology

Backend	Python 3.11, FastAPI

Storage	Custom LRU Cache

Persistence	Write‑Ahead Logging

Frontend	HTML, CSS, JavaScript

Auth	SessionMiddleware

Metrics	Custom counters

Replication	Async HTTP

Benchmarking	Python (requests, threading)

▶️ Running the Project

1️⃣ Install Dependencies

pip install fastapi uvicorn


2️⃣ Start Primary Node

$env:ROLE="primary"

$env:SECONDARY_URL="http://127.0.0.1:8001"

uvicorn main:app --port 8000


3️⃣ (Optional) Start Secondary Node

$env:ROLE="secondary"

uvicorn main:app --port 8001


4️⃣ Open in Browser

http://127.0.0.1:8000


🧪 Benchmarking

<p align="center"> <img src="assets/benchmark.png" width="650"/> </p>

python benchmark/benchmark.py

Outputs:


Throughput (ops/sec)

Latency

Concurrent load behavior

📊 Stats Dashboard

<p align="center"> <img src="assets/stats-ui.png" width="650"/> </p>

Metrics exposed via /stats:


Total keys

Cache hits

Evictions

TTL expirations

WAL size

Uptime

🧩 Why This Project Matters

This project demonstrates:


Real‑world cache design

Persistence strategies

Concurrency awareness

System observability

Backend‑frontend integration

Production‑level thinking

It is designed as a strong systems engineering portfolio piece, not just an academic assignment.

🔮 Future Enhancements
Snapshot + WAL hybrid recovery

Binary serialization (MsgPack)

Async replication streams

Leader election

Sharding

Docker support

Prometheus metrics

gRPC interface

👩‍💻 Author
Gupta Tripti
Backend & Systems Engineering Enthusiast

⭐ If you like this project
Give it a ⭐ on GitHub — it really helps!

