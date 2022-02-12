import pytest

from fastapi.testclient import TestClient
from entrypoints.fastapi.app import get_app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(get_app(do_mapping=False))