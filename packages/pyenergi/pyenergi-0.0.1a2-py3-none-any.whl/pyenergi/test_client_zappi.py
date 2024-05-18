import logging

import pytest

from . import exceptions
from .client import Hub

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.online
async def test_load_zappi_data():
    client = Hub()
    zappis = await client.get_zappis()
