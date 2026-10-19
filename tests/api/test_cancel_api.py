def make_order(client, auth_headers, product, quantity):
    response = client.post("/orders", json={"product_id": product.id, "quantity": quantity}, headers=auth_headers)
    return response.json()


def test_cancel_returns_200_and_cancelled_order(client, product, auth_headers):
    order = make_order(client, auth_headers, product, 3)

    response = client.post(f"/orders/{order['id']}/cancel", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_second_cancel_returns_409_and_keeps_stock(client, product, auth_headers):
    order = make_order(client, auth_headers, product, 3)
    client.post(f"/orders/{order['id']}/cancel", headers=auth_headers)
    stock_after_first = product.stock

    response = client.post(f"/orders/{order['id']}/cancel", headers=auth_headers)

    assert response.status_code == 409
    assert response.json() == {"detail": "이미 취소된 주문입니다."}
    assert product.stock == stock_after_first


def test_cancel_unknown_order_returns_404(client, auth_headers):
    response = client.post("/orders/77/cancel", headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "주문을 찾을 수 없습니다."}
