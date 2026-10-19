def test_create_order_returns_201_and_the_order(client, product, auth_headers):
    response = client.post("/orders", json={"product_id": product.id, "quantity": 2}, headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] == product.id
    assert body["quantity"] == 2
    assert body["total_price"] == 60000
    assert body["status"] == "created"


def test_get_order_returns_the_created_order(client, product, auth_headers):
    created = client.post("/orders", json={"product_id": product.id, "quantity": 1}, headers=auth_headers).json()

    response = client.get(f"/orders/{created['id']}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == created
