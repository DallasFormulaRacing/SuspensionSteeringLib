from WheelLoadHandler import WheelLoad
import pytest

@pytest.fixture
def test_wheel_load_calculations():
    
    return WheelLoad(
        x_LF = 0.0, 
        x_RF = 0.0, 
        x_RL = 0.0, 
        x_RR = 0.0, 
        filename="data\output2_linpot_2023-10-14_13-23-28.csv"
        )