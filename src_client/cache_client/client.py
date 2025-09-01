import socket

class CacheClient:
    def __init__(self, host="127.0.0.1", port=6379):
        self.host: str = host
        self.port: int = port
        self.socket: socket.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self
    
    def disconnect(self):
        if self.socket:
            self._send_command("QUIT")
            self.socket.close()
            self.socket = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.disconnect()
        return False

    def _send_command(self, command: str) -> str:
        if not self.socket:
            raise ConnectionError("no connection with server")
        
        self.socket.send(f"{command}\n".encode())
        response = self.socket.recv(1024).decode().strip()
        return response
    
    def set(self, key: str, value: str, seconds: float | None = None) -> str:
        command = f"SET {key} {value}"
        if seconds is not None:
            command += f" {float(seconds)}"
        return self._send_command(command)
    
    def get(self, key: str) -> str:
        command = f"GET {key}"
        return self._send_command(command)
    
    def expire(self, key: str, seconds: float) -> str:
        command = f"EXPIRE {key} {float(seconds)}"
        return self._send_command(command)
    
    def ttl(self, key: str) -> str:
        command = f"TTL {key}"
        return self._send_command(command)
    
    def pint(self) -> str:
        return self._send_command("PING")