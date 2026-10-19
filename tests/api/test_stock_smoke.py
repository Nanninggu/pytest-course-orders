def test_order_more_than_stock(client, product, auth_headers):
    response = client.post("/orders", json={"product_id": product.id, "quantity": 11}, headers=auth_headers)

    assert response.status_code == 409
    assert response.json() == {"detail": "재고가 부족합니다."}
    assert product.stock == 10
