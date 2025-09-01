import pytest
from unittest.mock import MagicMock, patch
from cache_server.server import CacheServer


class TestCacheServer:
    @pytest.fixture
    def cache_server(self):
        server = CacheServer("127.0.0.1", 6380)
        return server

    def test_handle_command(self, cache_server):
        response = cache_server.handle_command("SET test_key test_value")
        assert response.strip() == "True"

        response = cache_server.handle_command("GET test_key")
        assert response.strip() == "test_value"

        response = cache_server.handle_command("PING")
        assert response.strip() == "PONG"

        response = cache_server.handle_command("UNKNOWN_COMMAND")
        assert response.strip() == "unknown command"

    @patch("socket.socket")
    def test_start_server(self, mock_socket, cache_server):
        mock_server_socket = MagicMock()
        mock_socket.return_value = mock_server_socket

        cache_server.server_socket = mock_server_socket

        mock_server_socket.accept.side_effect = KeyboardInterrupt()

        cache_server.start()

        mock_server_socket.bind.assert_called_once_with(("127.0.0.1", 6380))
        mock_server_socket.listen.assert_called_once()
        mock_server_socket.accept.assert_called_once()
        mock_server_socket.close.assert_called_once()
