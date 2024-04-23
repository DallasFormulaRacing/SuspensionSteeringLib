import pandas as pd
import time
from ..Filter.filter import Filter
from ..conversions.conversion_factor_enum import Constants as constants
from ..calculations.calculations import Calculations

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
        self.acel_data = pd.DataFrame(pd.read_csv(filename2))

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

    def clean_acel_data(self):
        filter = Filter()
        self.acel_data = filter.butter_lowpass_filter(
            self.acel_data, "X", 4, 30, 2)
        self.acel_data = filter.butter_lowpass_filter(
            self.acel_data, "Y", 4, 30, 2)
        self.acel_data = filter.butter_lowpass_filter(
            self.acel_data, "Z", 4, 30, 2)

        return self.acel_data

    def convert_acel_to_g(self) -> pd.DataFrame:

        voltage_to_g = self.acel_data.copy()

        for i, row in self.acel_data.iterrows():
            voltage_to_g.loc[i, "X"] = (row["X"]) * 0.53
            voltage_to_g.loc[i, "Y"] = (row["Y"]) * 0.53
            voltage_to_g.loc[i, "Z"] = (row["Z"]) * 0.53

        return voltage_to_g

    def convert_time(self, data: pd.DataFrame) -> pd.DataFrame:
        for i, row in data.iterrows():
            time_step = row["Time"]
            if isinstance(time_step, str):
                break
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step))

        return data

    def convert_voltage_to_mm(self) -> pd.DataFrame:

        displacement_to_mm = self.data_linpot.copy()

        for i, row in displacement_to_mm.iterrows():
            displacement_to_mm.loc[i, "Front Right"] = (
                row["Front Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Front Left"] = -(row["Front Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Right"] = -(row["Rear Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Left"] = -(row["Rear Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET

        return displacement_to_mm

    def generate_pitch_roll_df(self, low_pass_data) -> pd.DataFrame:

        time = low_pass_data["Time"]
        x = low_pass_data["X_lowpass"]  # Accelerometer x values
        y = low_pass_data["Y_lowpass"]  # Accelerometer y values
        z = low_pass_data["Z_lowpass"]  # Accelerometer z values

        # Calculate pitch and roll angles
        pitch = []
        roll = []
        for i in range(len(x)):
            p, r = Calculations.calculate_pitch_roll_angles(x[i], y[i], z[i])
            pitch.append(p)
            roll.append(r)

        pitch_roll_df = pd.DataFrame({
            'Time': time,
            'Pitch': pitch,
            'Roll': roll
        })
        return pitch_roll_df