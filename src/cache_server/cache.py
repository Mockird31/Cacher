import time
import threading


class CacheStore:
    def __init__(self):
        self.store: dict[str, str] = {}
        self.expiry: dict[str, float] = {}
        self.lock = threading.Lock()

    def run_expiry_thread(self):
        def loop():
            while True:
                time.sleep(3600)
                with self.lock:
                    now = time.time()
                    expired_keys = [k for k, t in self.expiry.items() if now > t]
                    for k in expired_keys:
                        self.store.pop(k, None)
                        self.expiry.pop(k, None)
                    if expired_keys:
                        print(f"deleted expired keys: {expired_keys}")

        threading.Thread(target=loop, daemon=True).start()

    def set_data(self, key: str, value: str, expiry: str) -> bool:
        if key in self.store and key in self.expiry:
            self.expiry.pop(key, None)
        self.store[key] = value
        if expiry != "":
            self.expiry[key] = time.time() + float(expiry)
        return True

    def get_data(self, key: str) -> str:
        value = self.store.get(key)
        return value if value is not None else "nil"

    def expire(self, key: str, expiry: str) -> bool:
        if key in self.store:
            self.expiry[key] = time.time() + float(expiry)
            return True
        return False

    def ttl(self, key: str) -> int:
        if key not in self.store or key:
            return 0
        remaining_time = self.expiry.get(key, -1)
        return int(
            remaining_time if remaining_time == -1 else remaining_time - time.time()
        )
