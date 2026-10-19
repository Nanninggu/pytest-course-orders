import os

from app import services
from app.models import Product


def test_api_uses_the_test_db(client, db, auth_headers):
    db.add(Product(id=1, name="키보드", price=30000, stock=10))
    db.commit()
    services.create_order(db, 1, 2)

    response = client.get("/orders", headers=auth_headers)

    assert response.status_code == 200
    assert [order["total_price"] for order in response.json()] == [60000]
    assert not os.path.exists("orders.db")
