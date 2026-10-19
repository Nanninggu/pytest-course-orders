import pytest


@pytest.mark.parametrize("headers", [{}, {"X-API-Token": "wrong-token"}], ids=["no_token", "wrong_token"])
def test_request_without_valid_token_returns_401(client, headers):
    response = client.get("/orders", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "인증이 필요합니다."}


def test_request_with_token_returns_200(client, auth_headers):
    response = client.get("/orders", headers=auth_headers)

    assert response.status_code == 200
