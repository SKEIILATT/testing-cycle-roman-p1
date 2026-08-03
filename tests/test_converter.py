# test suite
import pytest

from roman.converter import (
    RomanError,
    to_roman,
    from_roman,
    is_valid_roman,
    add_roman,
    subtract_roman,
    _roundtrip_differs,
    _count_char,
)


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


def test_from_roman_four():
    assert from_roman("IV") == 4


def test_from_roman_nine():
    assert from_roman("IX") == 9


def test_from_roman_forty():
    assert from_roman("XL") == 40


def test_from_roman_ninety():
    assert from_roman("XC") == 90


def test_from_roman_four_hundred():
    assert from_roman("CD") == 400


def test_from_roman_nine_hundred():
    assert from_roman("CM") == 900


def test_from_roman_rejects_bad_pair():
    with pytest.raises(RomanError):
        from_roman("IL")


def test_from_roman_rejects_out_of_range():
    with pytest.raises(RomanError):
        from_roman("MMMM")


def test_is_valid_roman_true():
    assert is_valid_roman("XIV") is True


def test_is_valid_roman_false():
    assert is_valid_roman("XZ") is False


def test_add_roman_basic():
    assert add_roman("II", "II") == "IV"


def test_add_roman_rejects_out_of_range():
    with pytest.raises(RomanError):
        add_roman("MMM", "M")


def test_subtract_roman_basic():
    assert subtract_roman("X", "I") == "IX"


def test_subtract_roman_rejects_out_of_range():
    with pytest.raises(RomanError):
        subtract_roman("I", "I")


def test_roundtrip_differs_same():
    assert _roundtrip_differs(58, "LVIII") is False


def test_roundtrip_differs_not_same():
    assert _roundtrip_differs(58, "LIIX") is True


def test_count_char_found():
    assert _count_char("MMMCMXCIX", "M") == 4


def test_count_char_not_found():
    assert _count_char("MMMCMXCIX", "L") == 0
