# Automated Network Download Analyzer

## Overview
This project implements a secure client-server system using Python socket programming. Multiple clients simulate file downloads and send their statistics to a central server, which analyzes overall network performance.

The system uses **TLS (SSL) encryption** for secure communication and **multithreading** to handle multiple clients simultaneously.

---

## Features
- Secure communication using TLS/SSL
- Multi-client handling using threads
- Calculates:
  - Average speed
  - Maximum speed
  - Minimum speed
  - Total downloads
- Logs client data
- Measures response time

---

## Technologies Used
- Python
- TCP Socket Programming
- SSL/TLS (`ssl` module)
- Multithreading

---

# Automated Network Download Analyzer

## Overview
This project implements a secure client-server system using Python socket programming. Multiple clients simulate file downloads and send their statistics to a central server, which analyzes overall network performance.

The system uses **TLS (SSL) encryption** for secure communication and **multithreading** to handle multiple clients simultaneously.

---

## Features
- Secure communication using TLS/SSL
- Multi-client handling using threads
- Calculates:
  - Average speed
  - Maximum speed
  - Minimum speed
  - Total downloads
- Metrics Measured:
  - Download Speed
  - Latency (Download Time)
  - Throughput (Requests handled)
  - Response Time
- Logs client data
- Measures response time

---

## Technologies Used
- Python
- TCP Socket Programming
- SSL/TLS (`ssl` module)
- Multithreading

---

## Security Implementation

TLS is implemented using Python’s `ssl` module:

- Server:
  - Uses `SSLContext` with certificate (`server.crt`) and key (`server.key`)
  - Wraps socket using `wrap_socket()`

- Client:
  - Uses secure context to connect to server
  - Ensures encrypted communication

---

## ⚙️ How to Run

### Start Server and Run Client
```bash
python server.py
python client.py
