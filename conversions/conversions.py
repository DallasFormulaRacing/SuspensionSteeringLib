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

    def __init__(self, filename: str, filename2: str):
        self.filename = filename
        self.filename2 = filename2
        self.data_linpot = pd.DataFrame(pd.read_csv(filename))
        self.data_accel = pd.DataFrame(pd.read_csv(filename2))

        self.data_linpot = self.switch_columns(self.data_linpot)

    def switch_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )
        return df

    # todo return modifed dataframe that is passed in as an argument
    # todo change to new linpot orientation
    def switch_columns2(self):
        self.data_linpot = self.data_linpot.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm
    # todo return modifed dataframe that is passed in as an argument
    def convert_voltage_to_mm(self):
        for i, row in self.data_linpot.iterrows():
            self.data_linpot.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                      constants.LINPOT_CONVERSION_OFFSET)
            self.data_linpot.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) 
            self.data_linpot.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                     constants.LINPOT_CONVERSION_OFFSET) 
            self.data_linpot.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                    constants.LINPOT_CONVERSION_OFFSET)
        return self.data_linpot

    # converts voltage to mm and then inches for as spring rates are in inches / pound
    def convert_voltage_to_in(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df.iterrows():
            df.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                        constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            df.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                       constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            df.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                       constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            df.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                      constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        filter_instance = Filter()
        df = filter_instance.butter_lowpass_filter(df, "Front Right", 4, 30, 2)
        df = filter_instance.butter_lowpass_filter(df, "Front Left", 4, 30, 2)
        df = filter_instance.butter_lowpass_filter(df, "Rear Right", 4, 30, 2)
        df = filter_instance.butter_lowpass_filter(df, "Rear Left", 4, 30, 2)

        return df

    # todo return modifed dataframe that is passed in as an argument
    def convert_xl_g(self, df: pd.DataFrame) -> pd.DataFrame:
        for i, row in df.iterrows():
            df.loc[i, "X"] = (row["X"]) * constants.X_CONVERSION_CONSTANT_POS
            df.loc[i, "Y"] = (row["Y"]) * constants.Y_CONVERSION_CONSTANT_POS
            df.loc[i, "Z"] = (row["Z"]) * constants.Z_CONVERSION_CONSTANT_POS
        
        return df

    def convert_time(self, data: pd.DataFrame) -> pd.DataFrame:
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
        return data
    