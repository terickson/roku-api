from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from lib.config import Settings


@pytest.fixture()
def mock_settings():
    test_settings = Settings(
        log_level="DEBUG",
        log_module_name="roku-api-test",
        roku_hosts="living-room:192.168.1.10,bedroom:192.168.1.11",
        host="0.0.0.0",
        port=8080,
    )
    with patch("routes.roku.settings", test_settings):
        yield test_settings


@pytest.fixture()
def mock_roku_class():
    with patch("routes.roku.Roku") as mock_cls:
        mock_device = MagicMock()
        mock_app = MagicMock()
        mock_app.id = "12345"
        mock_app.name = "Netflix"
        mock_device.apps = [mock_app]
        mock_device.__getitem__ = MagicMock(return_value=MagicMock())
        mock_cls.return_value = mock_device
        yield mock_cls


@pytest.fixture()
def client(mock_settings, mock_roku_class):
    from server import app

    return TestClient(app)
