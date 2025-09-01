from cache_client.client import CacheClient

if __name__ == "__main__":
    with CacheClient() as client:
        print(client.set("another_key", "another_value"))
        print(client.get("another_key"))