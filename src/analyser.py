import socket
import ssl
import time
import json
from datetime import datetime
import os
import random

HOST = input("Enter Server IP (press Enter for localhost): ") or "127.0.0.1"
PORT = 5000
PATH = "/test"
RESULT_FILE = "../results/results.json"

INTERVAL = 15
DURATION = 150

CLIENT_ID = os.getpid()


def download():
    result = {
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "client_id": CLIENT_ID
    }

    try:
        # TCP
        t1 = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
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

        # HTTP request
        request = f"GET {PATH} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        # Receive
        t3 = time.time()
        data = b""

        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            data += chunk

        download_time = time.time() - t3

        # Validate response
        if not data.startswith(b"HTTP/1.1 200"):
            raise Exception("Invalid server response")

        # Extract body
        if b"\r\n\r\n" in data:
            body = data.split(b"\r\n\r\n", 1)[1]
        else:
            body = data

        size = len(body)

        if download_time > 0:
            speed = (size * 8) / (download_time * 1024 * 1024)
        else:
            speed = 0

        result.update({
            "success": True,
            "download_speed_mbps": speed,
            "download_time_seconds": download_time,
            "connection_time_ms": conn_time,
            "ssl_handshake_time_ms": ssl_time
        })

        print("=" * 40)
        print(f"[CLIENT {CLIENT_ID}] Speed: {speed:.2f} Mbps")
        print(f"Conn: {conn_time:.2f} ms | SSL: {ssl_time:.2f} ms | DL: {download_time:.2f} s")
        print("=" * 40)

        sock.close()

    except Exception as e:
        result["error"] = str(e)
        print("[ERROR]", e)

    return result


# Loop
start = time.time()
results = []

while time.time() - start < DURATION:
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Downloading...")

    r = download()
    results.append(r)

    os.makedirs("../results", exist_ok=True)

    with open(RESULT_FILE, "w") as f:
        json.dump({"results": results}, f, indent=4)

    time.sleep(INTERVAL + random.uniform(0, 2))