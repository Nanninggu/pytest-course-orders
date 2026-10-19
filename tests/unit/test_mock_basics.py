import pytest
from unittest.mock import MagicMock, Mock


def test_mock_returns_the_value_we_set():
    fake_charge = Mock(return_value={"status": "approved"})

    assert fake_charge(1, 60000) == {"status": "approved"}


def test_mock_accepts_any_attribute():
    fake = Mock()

    assert isinstance(fake.anything_at_all, Mock)


def test_magicmock_supports_len():
    with pytest.raises(TypeError):
        len(Mock())
    assert len(MagicMock()) == 0
