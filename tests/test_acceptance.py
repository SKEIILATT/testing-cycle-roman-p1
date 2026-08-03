# acceptance suite: criteria derived from SPECIFICATION.md, not from the code
from roman.converter import from_roman, is_valid_roman


def test_from_roman_trims_surrounding_whitespace():
    # Given a roman numeral surrounded by leading and trailing blank spaces
    # When from_roman is called with that string
    # Then it returns the numeral's value, per section 3 ("leading and
    # trailing whitespace is tolerated")
    assert from_roman("  IV  ") == 4


def test_is_valid_roman_rejects_non_canonical_form():
    # Given "IIII", which represents 4 but is not the canonical form of 4
    # When is_valid_roman is called with that string
    # Then it returns False, per section 4 ("the canonical form of 4 is IV")
    assert is_valid_roman("IIII") is False


def test_is_valid_roman_never_raises_on_non_string():
    # Given an input that is not a string, for example None
    # When is_valid_roman is called with that input
    # Then it returns False without raising, per section 6 ("it never raises,
    # for any type of input")
    assert is_valid_roman(None) is False
