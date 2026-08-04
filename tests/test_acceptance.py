# acceptance tests
import pytest

from roman.converter import from_roman, is_valid_roman, subtract_roman, RomanError


def test_from_roman_trims_surrounding_whitespace():
    assert from_roman("  IV  ") == 4


def test_is_valid_roman_rejects_non_canonical_form():
    assert is_valid_roman("IIII") is False


def test_subtract_roman_rejects_out_of_range_result():
    with pytest.raises(RomanError):
        subtract_roman("I", "I")
