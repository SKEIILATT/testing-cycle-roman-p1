# test suite
import pytest

from roman.converter import RomanError, to_roman, from_roman


def test_one():
    assert to_roman(1) == "I"


def test_two():
    assert to_roman(2) == "II"


def test_three():
    assert to_roman(3) == "III"


def test_five():
    assert to_roman(5) == "V"


def test_ten():
    assert to_roman(10) == "X"


def test_fifty():
    assert to_roman(50) == "L"


def test_hundred():
    assert to_roman(100) == "C"


def test_five_hundred():
    assert to_roman(500) == "D"


def test_thousand():
    assert to_roman(1000) == "M"


def test_from_one():
    assert from_roman("I") == 1


def test_from_five():
    assert from_roman("V") == 5


def test_from_two():
    assert from_roman("II") == 2


def test_roundtrip_small():
    assert from_roman(to_roman(7)) == 7


def test_roundtrip_medium():
    assert from_roman(to_roman(58)) == 58


def test_lowercase_input():
    assert from_roman("xi") == 11


def test_to_roman_rejects_float():
    with pytest.raises(RomanError):
        to_roman(3.5)


def test_to_roman_rejects_bool():
    with pytest.raises(RomanError):
        to_roman(True)


def test_to_roman_rejects_zero():
    with pytest.raises(RomanError):
        to_roman(0)


def test_to_roman_rejects_too_big():
    with pytest.raises(RomanError):
        to_roman(4000)


def test_from_roman_rejects_non_string():
    with pytest.raises(RomanError):
        from_roman(1994)


def test_from_roman_rejects_empty():
    with pytest.raises(RomanError):
        from_roman("")


def test_from_roman_rejects_bad_char():
    with pytest.raises(RomanError):
        from_roman("IIZ")
