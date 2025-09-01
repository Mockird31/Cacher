import pytest
from cache_server.cache import CacheStore


class TestCacheStore:
    @pytest.fixture
    def cache_store(self):
        return CacheStore()

    def test_set_and_get_data(self, cache_store):
        cache_store.set_data("key1", "value1", "")
        assert cache_store.get_data("key1") == "value1"
        assert cache_store.get_data("non_existent_key") == "nil"

    def test_set_with_expiry(self, cache_store):
        cache_store.set_data("key2", "value2", "1")
        assert cache_store.get_data("key2") == "value2"
        assert "key2" in cache_store.expiry

    def test_expire(self, cache_store):
        cache_store.set_data("key3", "value3", "")
        result = cache_store.expire("key3", "10")
        assert result is True
        assert "key3" in cache_store.expiry

        result = cache_store.expire("non_existent_key", "10")
        assert result is False

    def test_ttl(self, cache_store):
        cache_store.set_data("key4", "value4", "60")
        ttl = cache_store.ttl("key4")
        assert ttl > 0
        assert ttl <= 60

        cache_store.set_data("key5", "value5", "")
        assert cache_store.ttl("key5") == 0

        assert cache_store.ttl("non_existent_key") == 0
