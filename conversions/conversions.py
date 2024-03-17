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
        self.data = pd.DataFrame(pd.read_csv(filename))
        self.data2 = pd.DataFrame(pd.read_csv(filename2))

        self.data = self.switch_columns(self.data)

        print(self.data)
        print(self.data2.info())

    def switch_columns(self, df):
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
        self.data = self.data.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm
    # todo return modifed dataframe that is passed in as an argument
    def convert_voltage_to_mm(self):
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                               constants.LINPOT_CONVERSION_OFFSET)
            self.data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) 
            self.data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                              constants.LINPOT_CONVERSION_OFFSET) 
            self.data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                             constants.LINPOT_CONVERSION_OFFSET)
        return self.data

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
    def convert_xl_g(self):
        for i, row in self.data2.iterrows():
            self.data2.loc[i, "X"] = (row["X"]) * 0.51
            self.data2.loc[i, "Y"] = (row["Y"]) * 0.51310
            self.data2.loc[i, "Z"] = (row["Z"]) * 0.49

    def convert_time(self, data: pd.DataFrame) -> pd.DataFrame:
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
        return data
    