import socket
import threading
import os
from dotenv import load_dotenv
import tkinter as tk
from gui import ChatGUI

load_dotenv()

HOST = os.environ.get('CHAT_SERVER_HOST', '127.0.0.1')
PORT = int(os.environ.get('CHAT_SERVER_PORT', 5050))

nickname = input("Enter your nickname: ")

# Create a socket to establish a connection with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Creating tkinter window
root = tk.Tk()

chat_app = ChatGUI(root)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            display_message(message)
        except:
            break

# Function to display messages in the GUI text area
def display_message(message):
    chat_app.text_area.config(state="normal")
    chat_app.text_area.insert(tk.END, message)
    chat_app.text_area.config(state="disabled")

# Function to send a message to the server
def send_message():
    message = chat_app.input_area.get('1.0', 'end')
    if message:
        formatted_message = f"{nickname}: {message}"
        chat_app.input_area.delete('1.0', 'end')
        chat_app.text_area.config(state="normal")
        chat_app.text_area.insert(tk.END, formatted_message)
        chat_app.text_area.config(state="disabled")
        client_socket.send(formatted_message.encode('utf-8'))

chat_app.send_button.config(command=send_message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Function to close the socket and destroy the window
def close_socket():
    client_socket.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_socket)

root.mainloop()
