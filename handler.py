import pandas as pd
from Filter.filter import Filter
from conversion_equations.conversions import Conversions


class Handler:

    def __init__(self, df_linpots, df_imu):
        # base volatage for accelerometer
        self.df_accel = pd.read_csv(
            "data/output2_analog_2023-10-14_13-18-15.csv")
        # base volatage for linear potentiometers
        self.df_linpots = pd.read_csv(
            "data/output2_linpot_2023-10-14_13-23-28.csv")

        self.conversions_instance = Conversions()

    def clean_linpot_data(self) -> None:
        self.df_linpots = Filter.butter_lowpass_filter(
            self.df_linpots, "Front Right", 4, 30, 2)
        self.df_linpots = Filter.butter_lowpass_filter(
            self.df_linpots, "Front Left", 4, 30, 2)
        self.df_linpots = Filter.butter_lowpass_filter(
            self.df_linpots, "Rear Right", 4, 30, 2)
        self.df_linpots = Filter.butter_lowpass_filter(
            self.df_linpots, "Rear Left", 4, 30, 2)

    def linpot_data_transformation(self) -> pd.DataFrame:
        pass
