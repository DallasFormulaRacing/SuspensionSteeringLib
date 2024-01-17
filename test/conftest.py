import pytest
from conversions.py import conversions


@pytest_fixture
def test_conversion_functions():

    return conversions(
        file_name = "data/output2_analog_2023-10-14_13-18-15.csv"

    )
    
