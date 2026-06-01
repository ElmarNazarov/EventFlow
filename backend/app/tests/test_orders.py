import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _login(client: AsyncClient, email: str) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_viewer_cannot_create_order(client: AsyncClient):
    token = await _login(client, "viewer@eventflow.local")
    response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "customer_name": "Acme",
            "customer_email": "ops@acme.com",
            "items": [{"sku": "LAPTOP-PRO-14", "quantity": 1}],
        },
    )
    assert response.status_code == 403
