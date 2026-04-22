# Architecture

Client-Server Model using TCP sockets with SSL/TLS.

- Server:
  - Handles multiple clients using threading
  - Sends file using TCP

- Client:
  - Downloads file periodically
  - Measures speed, latency

Protocol:
- TCP socket
- HTTP request over TCP

Metrics:
- Throughput (Mbps)
- Latency
- Congestion detection