import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_login_requires_valid_credentials(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "missing@eventflow.local", "password": "wrong"},
    )
    assert response.status_code == 401
