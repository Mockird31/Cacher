from abc import ABC, abstractmethod
from cache_server.cache import CacheStore

type Response = bool | int | str


class Command(ABC):
    @abstractmethod
    def execute(self, store: CacheStore, args: list[str]) -> Response:
        pass


class SetCommand(Command):
    def execute(self, store: CacheStore, args: list[str]) -> Response:
        key, val, expiry = (args + [""])[:3]
        response = store.set_data(key, val, expiry)
        return response


class GetCommand(Command):
    def execute(self, store: CacheStore, args: list[str]) -> Response:
        key = args[0]
        val = store.get_data(key)
        return val


class ExpireCommand(Command):
    def execute(self, store: CacheStore, args: list[str]) -> Response:
        key, expire_time = args
        res = store.expire(key, expire_time)
        return res


class TTLCommand(Command):
    def execute(self, store: CacheStore, args: list[str]) -> Response:
        key = args[0]
        remaining_time = store.ttl(key)
        return remaining_time if remaining_time != 0 else "nil"
