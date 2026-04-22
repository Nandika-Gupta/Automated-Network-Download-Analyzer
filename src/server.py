import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 5000

FILE_DATA = b"A" * (3 * 1024 * 1024)


def handle_client(client, addr, context):
    try:
        # SSL handshake inside thread
        conn = context.wrap_socket(client, server_side=True)

        request = conn.recv(1024)

        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Length: " + str(len(FILE_DATA)).encode() + b"\r\n\r\n"
        response += FILE_DATA

        conn.sendall(response)

    except Exception as e:
        print("[ERROR]", e)

    finally:
        client.close()


def start():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("server.crt", "server.key")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  important fix
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(10)

    print("SERVER RUNNING on port", PORT)

    while True:
        client, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(client, addr, context)
        ).start()


if __name__ == "__main__":
    start()