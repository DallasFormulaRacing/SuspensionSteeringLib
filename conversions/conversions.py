import pandas as pd
<<<<<<< HEAD
from pandas import data_linpotFrame
import plotly.express as px
import time
from Filter.filter import Filter
from conversions import conversion_factor_enum
=======
from pandas import DataFrame
import time
from filter.filter import Filter
from conversions.conversion_factor_enum import Constants as constants
>>>>>>> refs/remotes/origin/3-accelerometer-graphs

# Add dampening to factor into the wheel loads. Depends on the velocity
# Dampening is proportional to velocity and it's a linear relationship


class Conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701
    ACCEL_G_CONSTANT = 1.0
    X_CONVERSION_CONSTANT_POS = 0.50381
    Y_CONVERSION_CONSTANT_POS = 0.51310
    Z_CONVERSION_CONSTANT_POS = 0.49961

    def __init__(self, filename_linpot: str, filename_acc: str):
        self.filename_linpot = filename_linpot
        self.data_linpot = pd.data_linpotFrame(pd.read_csv(filename_linpot))
        self.acc_data = pd.acc_dataFrame(pd.read_csv(filename_acc))
        self.switch_columns()
<<<<<<< HEAD
        
        print(self.data_linpot)

    def switch_columns(self):
        self.data_linpot = self.data_linpot.rename(
            columns = {
=======

        print(self.data)

    def switch_columns(self):
        self.data = self.data.rename(
            columns={
>>>>>>> refs/remotes/origin/3-accelerometer-graphs
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm and then inches for as spring rates are in inches / pound
    def convert_voltage_to_in(self):
<<<<<<< HEAD
        constants = conversion_factor_enum.Constants
        for i, row in self.data_linpot.iterrows():
            self.data_linpot.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data_linpot.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data_linpot.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data_linpot.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
=======
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                               constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                             constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
>>>>>>> refs/remotes/origin/3-accelerometer-graphs

    def clean_data_linpot(self):
        filter = Filter.Filter()
<<<<<<< HEAD
        self.data_linpot = filter.butter_lowpass_filter(self.data_linpot, "Front Right", 4, 30, 2)
        self.data_linpot = filter.butter_lowpass_filter(self.data_linpot, "Front Left", 4, 30, 2)
        self.data_linpot = filter.butter_lowpass_filter(self.data_linpot, "Rear Right", 4, 30, 2)
        self.data_linpot = filter.butter_lowpass_filter(self.data_linpot, "Rear Left", 4, 30, 2)
    
    def convert_voltage_to_gs(self):
        for i, row in self.data.iterrows():
            self.data.loc[i, "X"] = (row["X"] - self.x_basis) * self.X_CONVERSION_CONSTANT_POS
            self.data.loc[i, "Y"] = (row["Y"] - self.y_basis) * self.Y_CONVERSION_CONSTANT_POS
            self.data.loc[i, "Z"] = (row["Z"] - self.z_basis) * self.Z_CONVERSION_CONSTANT_POS

    def convert_time(self, data_linpot):
        for i, row in data_linpot.iterrows():
=======
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

    def convert_time(self, data):
        for i, row in data.iterrows():
>>>>>>> refs/remotes/origin/3-accelerometer-graphs
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data_linpot.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
    

