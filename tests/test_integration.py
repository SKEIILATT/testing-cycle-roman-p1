# integration suite: add_roman / subtract_roman built on from_roman + to_roman
from roman.converter import add_roman, subtract_roman, is_valid_roman


def test_add_roman_result_accepted_by_is_valid_roman():
    result = add_roman("MCMXCIV", "VI")
    assert result == "MM"
    assert is_valid_roman(result) is True


def test_subtract_roman_result_accepted_by_is_valid_roman():
    result = subtract_roman("X", "I")
    assert result == "IX"
    assert is_valid_roman(result) is True
