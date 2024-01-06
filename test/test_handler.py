import pytest

def test_voltage_to_g(test_conversions_functions):
    result = test_conversions_functions()
    assert result == 0