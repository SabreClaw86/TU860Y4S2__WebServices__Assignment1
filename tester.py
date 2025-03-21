from fastapi.testclient import TestClient
#from cryptography.fernet import Fernet

from httpx import AsyncClient
import pytest
from main import app  # Import your FastAPI app

client = TestClient(app)

baseurl = "http://localhost:8000"
#s = xmlrpc.client.ServerProxy('http://localhost:8000')

@pytest.mark.asyncio
async def test_get_all_products():
    async with AsyncClient(app=app, base_url=baseurl) as ac:
        response = await ac.get("/getAll")
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output


