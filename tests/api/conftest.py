import pytest
from fastapi.testclient import TestClient

from app.auth import API_TOKEN
from app.database import get_db
from app.main import app


@pytest.fixture
def client(db):
    """get_db를 테스트 세션으로 바꿔 끼운 TestClient."""

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    return {"X-API-Token": API_TOKEN}


@pytest.fixture
def broken_client():
    """DB 연결에서 예외가 나게 바꿔 끼운 TestClient."""

    def broken_get_db():
        raise RuntimeError("DB 연결 실패")

    app.dependency_overrides[get_db] = broken_get_db
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides.clear()
