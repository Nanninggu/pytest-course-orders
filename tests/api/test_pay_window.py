from datetime import datetime, timedelta

from app.models import Order


def test_pay_after_the_window_returns_409_and_does_not_charge(client, db, product, auth_headers, mocker):
    mock_charge = mocker.patch("app.services.charge")
    order = client.post("/orders", json={"product_id": product.id, "quantity": 1}, headers=auth_headers).json()
    db.get(Order, order["id"]).created_at = datetime.now() - timedelta(hours=25)
    db.commit()

    response = client.post(f"/orders/{order['id']}/pay", headers=auth_headers)

    assert response.status_code == 409
    assert response.json() == {"detail": "결제 기한이 지났습니다."}
    mock_charge.assert_not_called()
