import time

import pytest


@pytest.mark.parametrize("n", range(4))
def test_report_keeps_its_own_number(n, tmp_path):
    path = tmp_path / "report.txt"    # 테스트마다 자기만의 폴더를 쓴다
    path.write_text(str(n))
    time.sleep(0.3)    # 느린 처리를 흉내
    assert path.read_text() == str(n)
