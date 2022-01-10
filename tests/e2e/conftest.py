import pytest

from fastapi.testclient import TestClient
from entrypoints.fastapi.app import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
