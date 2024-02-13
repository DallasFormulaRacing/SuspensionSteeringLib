import pandas as pd
import time
from filter.filter import Filter
from conversions.conversion_factor_enum import Constants as constants

# Add dampening to factor into the wheel loads. Depends on the velocity
# Dampening is proportional to velocity and it's a linear relationship


class Conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701
    ACCEL_G_CONSTANT = 1.0

    def __init__(self, filename: str):
        self.filename = filename
        self.data = pd.DataFrame(pd.read_csv(filename))
        self.switch_columns()

        print(self.data)

    def switch_columns(self):
        self.data = self.data.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm and then inches for as spring rates are in inches / pound
    def convert_voltage_to_in(self):
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                               constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                             constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR

    def clean_data(self):
        filter = Filter()
        self.data = filter.butter_lowpass_filter(
            self.data, "Front Right", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(
            self.data, "Front Left", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(
            self.data, "Rear Right", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(
            self.data, "Rear Left", 4, 30, 2)

    def convert_xl_g(self):
        for i, row in self.xl_data.iterrows():
            self.xl_data.loc[i, "X"] = (row["X Axis"] - self.x_basis) * 0.53
            self.xl_data.loc[i, "Y"] = (row["Y Axis"] - self.y_basis) * 0.53
            self.xl_data.loc[i, "Z"] = (row["Z Axis"] - self.z_basis) * 0.53

    def convert_time(self, data_linpot):
        for i, row in data_linpot.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data_linpot.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
