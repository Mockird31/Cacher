import time


class CacheStore:
    def __init__(self):
        self.store: dict[str, str] = {}
        self.expiry: dict[str, float] = {}

    def check_key_expiry(self, key: str) -> None:
        if key in self.expiry and time.time() > self.expiry[key]:
            self.store.pop(key, None)
            self.expiry.pop(key, None)

    def set_data(self, key: str, value: str, expiry: float | None = None) -> bool:
        self.store[key] = value
        if expiry != None:
            self.expiry[key] = time.time() + expiry
        return True

    def get_data(self, key: str) -> str:
        value = self.store.get(key)
        return value if value is not None else "nil"
