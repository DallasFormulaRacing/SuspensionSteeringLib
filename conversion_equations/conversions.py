import pandas
from pandas import DataFrame
from Filter.filter import Filter


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

    def calculate_acceleration_conversion_factors(self):
        # calculate the variables for each axis
        pass

    def calculate_baseline_accel(self, x, y, z):
        # average the first 20 values from each axis
        # calculate the variable for each axis
        pass

    def convert_to_gs(self) -> DataFrame:
        # convert the voltage to gs
        pass

    def convert_voltage_to_mm(self) -> DataFrame:
        pass

    def calculate_wheel_load(self):
        pass
