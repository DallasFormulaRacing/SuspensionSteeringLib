import pandas
from pandas import DataFrame


class Conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    ACCEL_G_CONSTANT = 1.0
    FL_CORNER_WEIGHT = 150.0
    FR_CORNER_WEIGHT = 150.0
    RL_CORNER_WEIGHT = 150.0
    RR_CORNER_WEIGHT = 150.0

    def __init__(self):
        pass

    def convert_to_gs(self) -> DataFrame:
        # convert the voltage to gs
        pass

    def convert_voltage_to_mm(self) -> DataFrame:
        pass

    def calculate_wheel_load(self):
        pass
