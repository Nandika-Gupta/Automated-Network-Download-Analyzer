import socket
import ssl
import time
import random

SERVER_IP = "192.168.1.59"   # change to 192.168.x.x for other device
PORT = 5000

client_id = random.randint(1000, 9999)

print(f"Client {client_id} starting simulated download...")

file_size = random.randint(3, 8) * 1024 * 1024

start_time = time.time()

time.sleep(random.uniform(1, 3))

end_time = time.time()

download_time = end_time - start_time

speed = file_size / download_time / (1024 * 1024)

message = f"ClientID:{client_id} Size:{file_size} Time:{download_time:.2f} Speed:{speed:.2f}"

#  TLS context
context = ssl._create_unverified_context()

#  Wrap socket with TLS
client = context.wrap_socket(
    socket.socket(socket.AF_INET),
    server_hostname=SERVER_IP
)

client.connect((SERVER_IP, PORT))

print("Sending download statistics...")

client.sendall(message.encode())

client.close()

print("Download report sent to server.")