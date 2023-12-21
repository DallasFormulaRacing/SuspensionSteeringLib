import pytest

def test_constants(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_consts()
    assert(result[0] >= 243.10 and result[0] <= 243.5)
    #isinstance(result[0], float)
    