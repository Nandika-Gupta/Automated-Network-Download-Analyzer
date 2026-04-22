import socket
import ssl
import time
import json
from datetime import datetime
import os

HOST = input("Enter Server IP (press Enter for localhost): ") or "127.0.0.1"
PORT = 5000
PATH = "/test"
RESULT_FILE = "../results/results.json"

INTERVAL = 5
DURATION = 60


def download():
    result = {"timestamp": datetime.now().isoformat(), "success": False}

    try:
        # TCP connection
        t1 = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        conn_time = (time.time() - t1) * 1000

        print("✓ TCP connected")

        # SSL
        t2 = time.time()
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = context.wrap_socket(sock, server_hostname=HOST)
        ssl_time = (time.time() - t2) * 1000

        print(f"✓ SSL handshake ({ssl_time:.2f} ms)")
        print(f"Protocol: {sock.version()}")

        # HTTP request over TCP
        request = f"GET {PATH} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        # receive data
        t3 = time.time()
        data = b""

        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            data += chunk

        download_time = time.time() - t3

        # safe split
        if b"\r\n\r\n" in data:
            body = data.split(b"\r\n\r\n", 1)[1]
        else:
            body = data

        size = len(body)

        speed = (size * 8) / (download_time * 1024 * 1024)

        result.update({
            "success": True,
            "download_speed_mbps": speed,
            "download_time_seconds": download_time,
            "connection_time_ms": conn_time,
            "ssl_handshake_time_ms": ssl_time
        })

        print("="*40)
        print(f"Speed: {speed:.2f} Mbps")
        print("="*40)

    except Exception as e:
        result["error"] = str(e)
        print("[ERROR]", e)

    return result


# automated loop
start = time.time()
results = []

while time.time() - start < DURATION:
    print("\n--- Downloading ---")

    r = download()
    results.append(r)

    os.makedirs("../results", exist_ok=True)

    with open(RESULT_FILE, "w") as f:
        json.dump({"results": results}, f, indent=4)

    time.sleep(INTERVAL)