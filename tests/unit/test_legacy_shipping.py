import pytest

from app.legacy_shipping import calc_shipping

# 지금 동작을 그대로 적어 둔 테스트입니다(옳은지 그른지는 따지지 않습니다).
CASES = [
    ((0.5, "KR"), 3000),
    ((1, "KR"), 3000),
    ((3, "KR"), 5000),
    ((5, "KR"), 5000),
    ((10, "KR"), 9000),
    ((-1, "KR"), 3000),
    ((2, "US"), 19000),
    ((20, "US"), 55000),
    ((25, "US"), 71500.0),
    ((3, "CA"), 21000),
    ((30, "JP"), 25000),
    ((3, "KR", True), 10000),
    ((3, "KR", False, "FREE"), 0),
    ((10, "KR", False, "HALF"), 4500.0),
    ((3, "KR", False, "abc"), 5000),
]


@pytest.mark.parametrize("args, expected", CASES)
def test_current_behavior(args, expected):
    assert calc_shipping(*args) == expected
