import logging

import pytest

from . import exceptions
from .client import Hub

logger = logging.getLogger(__name__)


def test_credentials_constructor():
    """Pass in credentials via constructor."""
    serial_number = "foo"
    api_key = "bar"

    client = Hub(serial_number=serial_number, api_key=api_key)

    assert client.serial_number == serial_number
    assert client.api_key == api_key


def test_credentials_environment(monkeypatch):
    """Pass in credentials via environment variables."""
    serial_number = "foo"
    api_key = "bar"

    monkeypatch.setenv("PYENERGI_HUB_SERIAL_NUMBER", serial_number)
    monkeypatch.setenv("PYENERGI_API_KEY", api_key)

    client = Hub()

    assert client.serial_number == serial_number
    assert client.api_key == api_key


@pytest.mark.asyncio
@pytest.mark.online
async def test_invalid_hub():
    """Invalid hub serial number."""
    client = Hub(serial_number="INVALID", api_key="INVALID")
    with pytest.raises(exceptions.DirectorError) as e:
        await client.test()


@pytest.mark.asyncio
@pytest.mark.online
async def test_invalid_credentials():
    """Invalid API key for valid serial number."""
    client = Hub(serial_number="10642104", api_key="INVALID")
    with pytest.raises(exceptions.AuthenticationError) as e:
        await client.test()
