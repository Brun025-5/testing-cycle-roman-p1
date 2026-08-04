# test suite
import pytest

from roman.converter import (
    RomanError,
    to_roman,
    from_roman,
    is_valid_roman,
    _count_char,
    _roundtrip_differs,
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


# --- Part 3: Task 13 ---


def test_to_roman_non_integer_raises():
    with pytest.raises(RomanError):
        to_roman("10")


def test_to_roman_bool_raises():
    with pytest.raises(RomanError):
        to_roman(True)


def test_to_roman_below_min_raises():
    with pytest.raises(RomanError):
        to_roman(0)


def test_to_roman_above_max_raises():
    with pytest.raises(RomanError):
        to_roman(4000)


def test_from_roman_non_string_raises():
    with pytest.raises(RomanError):
        from_roman(123)


def test_from_roman_empty_string_raises():
    with pytest.raises(RomanError):
        from_roman("")


def test_from_roman_invalid_character_raises():
    with pytest.raises(RomanError):
        from_roman("ZZZ")


def test_from_roman_subtractive_pair():
    assert from_roman("MCMXCIV") == 1994


def test_from_roman_invalid_subtractive_pair_raises():
    with pytest.raises(RomanError):
        from_roman("IC")


def test_from_roman_out_of_range_raises():
    with pytest.raises(RomanError):
        from_roman("MMMM")


def test_is_valid_roman_true():
    assert is_valid_roman("XI") is True


def test_is_valid_roman_false():
    assert is_valid_roman("ZZZ") is False


def test_count_char():
    assert _count_char("MMXX", "M") == 2


def test_roundtrip_differs_true():
    assert _roundtrip_differs(4, "wrong") is True


def test_roundtrip_differs_false():
    assert _roundtrip_differs(1, "I") is False
