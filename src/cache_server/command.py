from abc import ABC, abstractmethod
from cache import CacheStore

type Response = bool | int


class Command(ABC):
    @abstractmethod
    def execute(self, store: CacheStore, args: tuple[str]) -> Response:
        pass


class SetCommand(Command):
    def execute(self, store: CacheStore, args: tuple[str]) -> Response:
        pass


class GetCommand(Command):
    def execute(self, store: CacheStore, args: tuple[str]) -> Response:
        pass
