class RomanError(ValueError):
    pass


_PAIRS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


_SINGLE = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


_VALID_SUBTRACTIVE = {"IV", "IX", "XL", "XC", "CD", "CM"}


_MIN_VALUE = 1
_MAX_VALUE = 3999


def to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise RomanError("value must be an integer")
    if n < _MIN_VALUE:
        raise RomanError("value must be >= 1")
    if n > _MAX_VALUE:
        raise RomanError("value must be <= 3999")
    out = []
    remaining = n
    for value, symbol in _PAIRS:
        while remaining >= value:
            out.append(symbol)
            remaining -= value
    return "".join(out)


def from_roman(s):
    if not isinstance(s, str):
        raise RomanError("value must be a string")
    text = s.upper()
    if text == "":
        raise RomanError("empty string is not a roman numeral")
    for ch in text:
        if ch not in _SINGLE:
            raise RomanError("invalid roman character: " + ch)
    total = 0
    i = 0
    length = len(text)
    while i < length:
        if i + 1 < length:
            pair = text[i:i + 2]
            if pair in _VALID_SUBTRACTIVE:
                total += _SINGLE[pair[1]] - _SINGLE[pair[0]]
                i += 2
                continue
        current = _SINGLE[text[i]]
        if i + 1 < length:
            nxt = _SINGLE[text[i + 1]]
            if current < nxt:
                raise RomanError("invalid subtractive pair: " + text[i:i + 2])
        total += current
        i += 1
    if total < _MIN_VALUE or total > _MAX_VALUE:
        raise RomanError("value out of range 1..3999")
    return total


def _roundtrip_differs(value, text):
    return to_roman(value) != text


def _count_char(text, ch):
    total = 0
    for c in text:
        if c == ch:
            total += 1
    return total


def is_valid_roman(s):
    try:
        from_roman(s)
        return True
    except RomanError:
        return False


def add_roman(a, b):
    return to_roman(from_roman(a) + from_roman(b))


def subtract_roman(a, b):
    return to_roman(from_roman(a) - from_roman(b))
