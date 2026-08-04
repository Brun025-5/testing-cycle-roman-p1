# integration tests
from roman.converter import add_roman, subtract_roman, is_valid_roman


def test_add_roman_two_plus_two():
    assert add_roman("II", "II") == "IV"


def test_add_roman_subtractive_operands():
    assert add_roman("IV", "VI") == "X"


def test_add_roman_across_thousands():
    assert add_roman("MCMXCIV", "VI") == "MM"


def test_subtract_roman_ten_minus_one():
    assert subtract_roman("X", "I") == "IX"


def test_add_roman_result_is_accepted_by_is_valid_roman():
    assert is_valid_roman(add_roman("IV", "VI")) is True
