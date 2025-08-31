from cache import CacheStore
from command import *


class CacheServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host: str = host
        self.port: int = port
        self.cache_store: CacheStore = CacheStore()
        self.commands: dict[str, Command] = {
            "SET": SetCommand(),
            "GET": GetCommand(),
        }

    def handle_command(self, data: str) -> str:
        parts_data = data.split()
        comm = self.commands.get(parts_data[0])
        if comm is None:
            return "unknown command"
        res = comm.execute(self.cache_store, parts_data)
        return str(res)
