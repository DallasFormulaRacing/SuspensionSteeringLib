import pandas as pd
from pandas import DataFrame
import plotly.express as px
import time
from Filter import Filter
from conversions import conversion_factor_enum

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
            columns = {
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    # converts voltage to mm and then inches for as spring rates are in inches / pound
    def convert_voltage_to_in(self):
        constants = conversion_factor_enum.Constants
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = (-(row["Front Right"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Front Left"] = (-(row["Front Left"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Right"] = (-(row["Rear Right"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR
            self.data.loc[i, "Rear Left"] = (-(row["Rear Left"] * constants.LINPOT_CONVERSION_CONSTANT) + constants.LINPOT_CONVERSION_OFFSET) * constants.MM_TO_IN_CONVERSION_FACTOR

    def clean_data(self):
        filter = Filter.Filter()
        self.data = filter.butter_lowpass_filter(self.data, "Front Right", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(self.data, "Front Left", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(self.data, "Rear Right", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(self.data, "Rear Left", 4, 30, 2)
    
    def convert_to_gs(self) -> DataFrame:
        # convert the voltage to gs
        pass
   
    def convert_time(self, data):
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
