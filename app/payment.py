import os
import uuid

import requests

DEFAULT_PAYMENT_URL = "https://pay.example.com"


class PaymentError(Exception):
    pass


class PaymentDeclined(PaymentError):
    pass


class PaymentTimeout(PaymentError):
    pass


def payment_url() -> str:
    return os.environ.get("PAYMENT_URL", DEFAULT_PAYMENT_URL)


def charge(order_id: int, amount: int) -> dict:
    """외부 결제 서비스에 결제를 요청하고 승인 결과를 돌려준다."""
    api_key = os.environ["PAYMENT_API_KEY"]
    try:
        response = requests.post(
            f"{payment_url()}/v1/charges",
            json={"order_id": order_id, "amount": amount},
            headers={"Authorization": f"Bearer {api_key}", "Idempotency-Key": str(uuid.uuid4())},
            timeout=3,
        )
    except requests.Timeout:
        raise PaymentTimeout(order_id)
    except requests.ConnectionError:
        raise PaymentError(f"{payment_url()} 에 연결할 수 없습니다") from None
    if response.status_code == 402:
        raise PaymentDeclined(order_id)
    if response.status_code != 200:
        raise PaymentError(response.status_code)
    return response.json()
