import socket
import threading
import datetime
from dotenv import load_dotenv

load_dotenv()


class ChatServer:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(2)

        # Store connected client socket objects
        self.clients = []

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                client_name = f"Client {self.clients.index(client_socket) + 1}"
                print(f"Received message from {client_name}: {message}")

                # Save message to a file
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(f"client_{client_name}_{addr[1]}.txt", "a") as file:
                    file.write(f"[{timestamp}] {message}")

                for client in self.clients:
                    if client != client_socket:
                        client.send(message.encode('utf-8'))
            except:
                break

    def client_acceptance_thread(self):
        print("Server is listening...")
        try:
            while True:
                try:
                    # Accept incoming client connection
                    client_socket, addr = self.server.accept()
                    self.clients.append(client_socket)
                    print(f"Connected to {addr}")
                    # Create thread to handle client communication
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.start()
                except OSError as e:
                    if e.errno == 10038:
                        break
        except KeyboardInterrupt:
            pass

    def shutdown_server(self):
        print("Shutting down the server...")
        for client_socket in self.clients:
            client_socket.close()

        self.server.close()
        print("Server shut down.")

