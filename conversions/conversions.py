import pandas as pd
import time
from filter.filter import Filter
from conversions.conversion_factor_enum import Constants as constants
from calculations.calculations import Calculations

# Add dampening to factor into the wheel loads. Depends on the velocity
# Dampening is proportional to velocity and it's a linear relationship


class Conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701
    ACCEL_G_CONSTANT = 1.0

    def __init__(self, linpot_filename: str, acel_filename: str):
        self.linpot_filename = linpot_filename
        self.acel_filename = acel_filename
        self.linpot_data = pd.read_csv(linpot_filename)
        self.acel_data = pd.read_csv(acel_filename)
        self.switch_columns()

    def switch_columns(self):
        self.linpot_data = self.linpot_data.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm and then inches for as spring rates are in inches / pound
    def convert_voltage_to_in(self) -> pd.DataFrame:

        displacement_to_inches = self.linpot_data.copy()

        for i, row in displacement_to_inches.iterrows():
            displacement_to_inches.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                            constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            displacement_to_inches.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                           constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            displacement_to_inches.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                           constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            displacement_to_inches.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) +
                                                          constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR

        return displacement_to_inches

    def convert_voltage_to_mm(self) -> pd.DataFrame:

        displacement_to_mm = self.linpot_data.copy()

        for i, row in displacement_to_mm.iterrows():
            displacement_to_mm.loc[i, "Front Right"] = (
                row["Front Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Front Left"] = -(row["Front Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Right"] = -(row["Rear Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Left"] = -(row["Rear Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET

        return displacement_to_mm

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

    def convert_time(self, linpot_data):
        for i, row in linpot_data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            linpot_data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )

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
