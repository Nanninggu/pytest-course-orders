def test_list_orders_returns_the_seeded_orders(client, seeded, auth_headers):
    response = client.get("/orders", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert [o["id"] for o in body] == [o.id for o in seeded.orders]
    assert body[1]["total_price"] == 45000
