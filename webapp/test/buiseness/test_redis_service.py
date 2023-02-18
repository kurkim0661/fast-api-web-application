"""Tests module."""

from unittest import mock

import pytest
from httpx import AsyncClient

from webapp.main.application import app, container
from webapp.main.containers import Container
from webapp.main.buiseness import redis_service


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_index(client):
    service_mock = mock.AsyncMock(spec=redis_service.Service)
    service_mock.process.return_value = "Foo"

    with container.redis_service.override(service_mock):
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"result": "Foo"}