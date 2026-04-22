#  Automated Network Download Analyzer

## 📌 Project Overview
This project implements a **secure, automated client-server system** using low-level **TCP socket programming in Python**.

Multiple clients periodically download a file from a central server, measure network performance metrics, and send the results back for **analysis of congestion patterns over time**.

The system simulates **real-world network load conditions** and helps identify **performance variations and busiest network periods**.

---

##  Problem Statement
Network performance varies due to congestion, user load, and time-based usage patterns.

This project aims to:
- Automate periodic file downloads  
- Measure performance metrics (speed, latency, throughput)  
- Analyze trends to detect **network congestion patterns**

---

##  System Architecture

### 🔹 Client
- Periodically downloads a test file (scheduled execution)
- Measures:
  - Download speed  
  - Latency (download time)  
  - Response time  
- Sends metrics securely to the server using TLS

### 🔹 Server
- Handles **multiple clients concurrently** using threading  
- Receives and processes client data  
- Logs and aggregates performance metrics  
- Uses secure SSL/TLS communication  

---

##  Security Implementation
- Uses Python `ssl` module for **TLS encryption**

**Server:**
- Creates `SSLContext`
- Loads certificate (`server.crt`) and key (`server.key`)
- Wraps socket using `wrap_socket()`

**Client:**
- Establishes secure TLS connection with server  

Ensures **encrypted communication over TCP**

---

##  Core Features
- Low-level TCP socket programming (`AF_INET`, `SOCK_STREAM`)
- Secure communication using TLS/SSL  
- Multi-client handling using threading  
- Automated periodic downloads  
- Centralized performance analysis  

---

##  Metrics Measured
- **Throughput (Mbps)** – data transfer rate  
- **Latency** – time taken for download completion  
- **Response Time** – server responsiveness  
- **Download Speed Statistics**:
  - Average speed  
  - Maximum speed  
  - Minimum speed  
- **Total downloads per client**

---

##  Performance Evaluation
- Simulates **multiple concurrent clients**
- Analyzes:
  - Network congestion patterns  
  - Peak usage periods (busiest hour)  
  - Performance variation over time  

Outputs:
- Logs  
- Statistical summaries  
- Graphs 

---

##  Technologies Used
- Python  
- TCP Socket Programming  
- SSL/TLS (`ssl` module)  
- Multithreading  
- JSON / Logging  

---

## How to Run

### 1. Start Server
```bash
python server.py
```

### 2. Run Client(s)
```bash
python analyser.py
python report.py
```
--- 
##  Conclusion
This project demonstrates a secure, scalable, and automated network monitoring system that analyzes performance trends and detects congestion patterns effectively.
