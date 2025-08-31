from cache_server.cache import CacheStore
from cache_server.command import (
    Command,
    SetCommand,
    GetCommand,
    ExpireCommand,
    TTLCommand,
)
import socket


class CacheServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host: str = host
        self.port: int = port
        self.cache_store: CacheStore = CacheStore()
        self.commands: dict[str, Command] = {
            "SET": SetCommand(),
            "GET": GetCommand(),
            "EXPIRE": ExpireCommand(),
            "TTL": TTLCommand(),
        }

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_command(self, data: str) -> str:
        parts_data = data.split()
        comm = self.commands.get(parts_data[0])
        if comm is None:
            return "unknown command"
        res = comm.execute(self.cache_store, parts_data[1:])
        return str(res) + "\n"

    def handle_client(self, client_socket: socket.socket, client_address):
        print(f"Connection from {client_address}")

        try:
            while True:
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break

                if data.split()[0] == "QUIT":
                    client_socket.send("QUIT FROM SERVER\n".encode())
                    return

                response = self.handle_command(data)
                client_socket.send(response.encode())
        finally:
            client_socket.close()
            print(f"Connection closed with {client_address}")

    def start(self):
        self.cache_store.run_expiry_thread()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"server running on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("shutting down server..")
        finally:
            self.server_socket.close()
