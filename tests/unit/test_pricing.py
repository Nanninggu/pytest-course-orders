from app.pricing import discount_rate


def test_member_bulk_order_gets_eight_percent():
    assert discount_rate(10, True) == 8


def test_non_member_bulk_order_gets_three_percent():
    assert discount_rate(10, False) == 3


def test_member_small_order_gets_five_percent():
    assert discount_rate(9, True) == 5
