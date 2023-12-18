import pandas
from pandas import DataFrame


class conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    ACCEL_G_CONSTANT = 1.0

    def __init__(self):
        df_accel = pandas.read_csv("")  # base volatage for accelerometer
        # base volatage for linear potentiometers
        def_linpots = pandas.read_csv("")
        # initlaize with base line voltages for x, y, and z

    def calculate_acceleration_conversion_factors(self):
        # calculate the variables for each axis
        pass

    def calculate_baseline_accel(self, x, y, z):
        # average the first 20 values from each axis
        # calculate the variable for each axis
        pass

    def convert_to_gs(self):
        # convert the voltage to gs
        pass

    def convert_voltage_to_mm(self) -> DataFrame:
        pass

    def calculate_wheel_load(self):
        pass

    # def apply_low_pass_filter(self):
    #     pass
