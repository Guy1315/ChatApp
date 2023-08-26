import socket
import threading
import datetime 
from collections import defaultdict
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

        # Store messages sent by clients (address -> [(timestamp, message)])
        self.client_messages = defaultdict(list)

        self.message_counts = defaultdict(int)

        # Store the longest message from each client (address -> message)
        self.longest_messages = {}

        # Store client socket objects by address (address -> socket)
        self.client_sockets = {}

        
    def handle_client(self, client_socket, addr):

            # Dictionary to keep track of the message counts for each client
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
                        file.write(f"[{timestamp}] {message}\n")

                    # Increment message count for the client
                    self.message_counts[addr] += 1

                    self.client_sockets[addr] = client_socket  # Store client socket  

                    # Update client_messages dictionary
                    self.client_messages[addr].append((timestamp, message))   

                    # Update longest message for the client
                    self.longest_messages[addr] = max(message, self.longest_messages.get(addr, ''), key=len)

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

    #Find and print the longest messages sent by clients.
    def find_longest_messages(self):
        if self.longest_messages:
            print("Longest message from both clients:")
            print(max(self.longest_messages.values(), key=len))
        else:
            print("No messages found.")

            
    def print_messages_in_time_frame(self, start_time, end_time):

        print("Messages sent between", start_time, "and", end_time)
        
        # Collect all messages from the client_messages dictionary and sort them by timestamp
        all_messages = [msg for messages in self.client_messages.values() for msg in messages]
        all_messages = sorted(all_messages, key=lambda x: x[0])
        
        # Go through each message and its timestamp
        for timestamp, message in all_messages:
            # Convert the timestamp string to a datetime object
            message_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            if start_time <= message_time <= end_time:
                print(f"[{timestamp}] {message}")
            elif message_time > end_time:
                break
            
    # Get the name of the client associated with the given address
    def get_client_name(self, client_addr):
        client_socket = self.client_sockets[client_addr]
        index = self.clients.index(client_socket)
        return f"Client {index + 1}"



