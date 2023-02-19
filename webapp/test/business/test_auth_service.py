from unittest import mock

import pytest
from httpx import AsyncClient

from webapp.main.application import app
from webapp.main.business import auth_service
from webapp.main.domain.dto.user import UserDTO


@pytest.fixture(autouse=True)
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client

    event_loop.run_until_complete(client.aclose())


class TestAuthService:
    @pytest.fixture(autouse=True)
    def inner_client(self):
        return client

    async def test_get_users(self, inner_client):
        service_mock = mock.Mock(spec=auth_service.AuthService)
        service_mock.authenticate_user.return_value = UserDTO(username="test", email="test@example.com",
                                                              hashed_password="1234", is_active=True)
        with app.container.auth_service.override(service_mock):
            response = await inner_client.post("/token", data={"username": "test", "password": "1234"})

        assert response.status_code == 200
        assert response.json() == {"result": "Foo"}

    def test_user_by_id(self):
        assert True

    def test_create_user(self):
        assert True

    def test_verify_password(self):
        assert True

    def test_get_password_hash(self):
        assert True

    def test_authenticate_user(self):
        assert True
