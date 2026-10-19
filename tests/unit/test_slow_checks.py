import time

import pytest


def slow_double(n):
    time.sleep(0.5)    # 외부 서비스의 응답을 기다리는 느린 처리라고 가정
    return n * 2


@pytest.mark.parametrize("n", range(8))
def test_slow_double(n):
    assert slow_double(n) == n * 2
