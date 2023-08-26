import socket
import threading
import os
from dotenv import load_dotenv
load_dotenv()

# Client configuration
HOST = os.environ.get('CHAT_SERVER_HOST', '127.0.0.1')
PORT = int(os.environ.get('CHAT_SERVER_PORT', 5050))

# Receive and display messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

# input and send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        
# socket to establish a connection with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# thread to send messages to the server
send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()