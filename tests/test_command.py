import pytest
from unittest.mock import MagicMock, patch
from cache_server.cache import CacheStore
from cache_server.command import (
    SetCommand,
    GetCommand,
    ExpireCommand,
    TTLCommand,
    PINGCommand,
)


class TestCommands:
    @pytest.fixture
    def cache_store(self):
        return CacheStore()

    def test_set_command(self, cache_store):
        cmd = SetCommand()
        result = cmd.execute(cache_store, ["key1", "value1"])
        assert result is True
        assert cache_store.get_data("key1") == "value1"

        result = cmd.execute(cache_store, ["key2", "value2", "10"])
        assert result is True
        assert "key2" in cache_store.expiry

    def test_get_command(self, cache_store):
        cache_store.set_data("key1", "value1", "")
        cmd = GetCommand()
        result = cmd.execute(cache_store, ["key1"])
        assert result == "value1"

        result = cmd.execute(cache_store, ["non_existent_key"])
        assert result == "nil"

    def test_expire_command(self, cache_store):
        cache_store.set_data("key1", "value1", "")
        cmd = ExpireCommand()
        result = cmd.execute(cache_store, ["key1", "10"])
        assert result is True
        assert "key1" in cache_store.expiry

    def test_ttl_command(self, cache_store):
        cache_store.set_data("key1", "value1", "60")
        cmd = TTLCommand()
        result = cmd.execute(cache_store, ["key1"])
        assert isinstance(result, int) or result == "nil"

        cache_store.set_data("key2", "value2", "")
        result = cmd.execute(cache_store, ["key2"])
        assert result == -1 or result == "nil"

    def test_ping_command(self, cache_store):
        cmd = PINGCommand()
        result = cmd.execute(cache_store, [])
        assert result == "PONG"
