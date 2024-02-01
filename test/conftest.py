from Depreciated.WheelLoadHandler import WheelLoad
import pytest


@pytest.fixture
def test_wheel_load_calculations():
    return WheelLoad(
        filename="data\\output2_linpot_2023-10-14_13-23-28.csv"
        )
