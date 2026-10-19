def test_unknown_product_returns_404(client, auth_headers):
    response = client.post("/orders", json={"product_id": 99, "quantity": 1}, headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "상품을 찾을 수 없습니다."}


def test_unknown_order_returns_404(client, auth_headers):
    response = client.get("/orders/77", headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "주문을 찾을 수 없습니다."}


def test_zero_quantity_returns_422(client, auth_headers):
    response = client.post("/orders", json={"product_id": 1, "quantity": 0}, headers=auth_headers)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "quantity"]


def test_missing_product_id_returns_422(client, auth_headers):
    response = client.post("/orders", json={"quantity": 2}, headers=auth_headers)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "product_id"]


def test_database_failure_returns_500(broken_client, auth_headers):
    response = broken_client.get("/orders", headers=auth_headers)

    assert response.status_code == 500
    assert response.json() == {"detail": "서버 오류가 발생했습니다."}
