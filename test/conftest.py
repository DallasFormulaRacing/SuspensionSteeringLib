import pytest
from conversion_equations import conversions
from handler import handler

@pytest.fixture
def test_conversions():
    return conversions (
        file_name = "data/output2_analog_2023-10-14_13-18-15.csv"
    )

@pytest.fixture
def test_handler():
    return handler(
        file_name = "data/output2_analog_2023-10-14_13-18-15.csv"
    )