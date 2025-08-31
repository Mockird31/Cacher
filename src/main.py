from cache_server.server import CacheServer

if __name__ == "__main__":
    server = CacheServer("0.0.0.0")
    server.start()
