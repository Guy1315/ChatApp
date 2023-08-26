from server import ChatServer
import threading
from utils import run_post_shutdown_tasks
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    HOST = os.environ.get('CHAT_SERVER_HOST', '127.0.0.1')
    PORT = int(os.environ.get('CHAT_SERVER_PORT', 5050))

    server = ChatServer(HOST, PORT)
    
    # thread to handle incoming client connections
    accept_thread = threading.Thread(target=server.client_acceptance_thread)
    accept_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown_server()
        run_post_shutdown_tasks(server)

if __name__ == "__main__":
    main()
