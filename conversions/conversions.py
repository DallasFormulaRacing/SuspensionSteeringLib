import pandas as pd
import time
from Filter.Filter import Filter
from conversions.conversion_factor_enum import Constants as constants

# Add dampening to factor into the wheel loads. Depends on the velocity
# Dampening is proportional to velocity and it's a linear relationship


class Conversions:

    def __init__(self, filename: str, xcel_filename: str):
        self.filename = filename
        self.data = pd.DataFrame(pd.read_csv(filename))
        self.xcel_data = pd.DataFrame(pd.read_csv(xcel_filename))
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
        for i, row in self.linpot_data.iterrows():
            self.linpot_data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                      constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                    constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR

    def convert_voltage_to_mm(self):
        for i, row in self.linpot_data.iterrows():
            self.linpot_data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                      constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.linpot_data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                    constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR

    def clean_linpot_data(self):
        filter = Filter()
        self.linpot_data = filter.butter_lowpass_filter(
            self.linpot_data, "Front Right", 4, 30, 2)
        self.linpot_data = filter.butter_lowpass_filter(
            self.linpot_data, "Front Left", 4, 30, 2)
        self.linpot_data = filter.butter_lowpass_filter(
            self.linpot_data, "Rear Right", 4, 30, 2)
        self.linpot_data = filter.butter_lowpass_filter(
            self.linpot_data, "Rear Left", 4, 30, 2)

    def convert_acel_to_g(self):
        for i, row in self.acel_data.iterrows():
            self.acel_data.loc[i, "X"] = (row["X"]) * 0.53
            self.acel_data.loc[i, "Y"] = (row["Y"]) * 0.53
            self.acel_data.loc[i, "Z"] = (row["Z"]) * 0.53
                   
    def convert_time(self, linpot_data):
        for i, row in linpot_data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            linpot_data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )

    def convert_voltage_to_gs(self):
        for i, row in self.data.iterrows():
            self.xcel_data.loc[i, "X"] = (row["X"]) * constants.X_CONVERSION_CONSTANT_POS
            self.xcel_data.loc[i, "Y"] = (row["Y"]) * constants.Y_CONVERSION_CONSTANT_POS
            self.xcel_data.loc[i, "Z"] = (row["Z"]) * constants.Z_CONVERSION_CONSTANT_POS
