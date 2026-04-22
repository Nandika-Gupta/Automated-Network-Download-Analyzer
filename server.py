import socket
import threading
import ssl

HOST = "0.0.0.0"
PORT = 5000

active_clients = 0
total_downloads = 0
speeds = []

lock = threading.Lock()


def handle_client(conn, addr):
    global active_clients, total_downloads

    print(f"\nClient connected: {addr}")

    try:
        data = conn.recv(1024)

        if not data:
            print("No data received")
            conn.close()
            return

        message = data.decode().strip()

        parts = message.split()

        client_id = parts[0].split(":")[1]
        size = int(parts[1].split(":")[1])
        time_taken = float(parts[2].split(":")[1])
        speed = float(parts[3].split(":")[1])

        print("\n----- CLIENT DOWNLOAD REPORT -----")
        print(f"Client ID: {client_id}")
        print(f"Client Address: {addr}")
        print(f"File Size: {size} bytes")
        print(f"Download Time: {time_taken} seconds")
        print(f"Download Speed: {speed:.2f} MB/s")
        print("----------------------------------")

        with lock:
            speeds.append(speed)
            total_downloads += 1

            avg_speed = sum(speeds) / len(speeds)
            max_speed = max(speeds)
            min_speed = min(speeds)

        print("\n===== NETWORK DOWNLOAD ANALYZER =====")
        print(f"Active Clients: {active_clients}")
        print(f"Total Downloads: {total_downloads}")
        print(f"Average Speed: {avg_speed:.2f} MB/s")
        print(f"Max Speed: {max_speed:.2f} MB/s")
        print(f"Min Speed: {min_speed:.2f} MB/s")
        print("=====================================\n")

        with open("logs/downloads.txt", "a") as f:
            f.write(f"{addr} -> {message}\n")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()

        with lock:
            active_clients -= 1

        print(f"Client disconnected: {addr}")


# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print("Secure Server running on port 5000...")

# TLS / SSL configuration
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

while True:
    conn, addr = server.accept()

    # Wrap socket with TLS encryption
    secure_conn = context.wrap_socket(conn, server_side=True)

    with lock:
        active_clients += 1

    thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
    thread.start()