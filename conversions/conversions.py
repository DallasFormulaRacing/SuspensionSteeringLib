import pandas as pd
from pandas import DataFrame
import plotly.express as px
import time
from sklearn.cluster import KMeans
from Filter import Filter
from conversions import conversion_factor_enum

# Add dampening to factor into the wheel loads. Depends on the velocity 
# Dampening is proportional to velocity and it's a linear relationship

class Conversions:
    
    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701
    #ACCEL_G_CONSTANT = 1.0    This was not being used
    ANALOG_ACCEL_CONVERSION_CONSTANT = 0.3
    ANALOG_ACCEL_CONVERSION_OFFSET = 1.5
    Gs_TO_METERS_PER_SEC_SQUARED_CONVERSION_FACTOR = 9.81

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

    #Performing conversions on accelerometer data
    def clean_accelerometer_data(self):
        filter = Filter.filter()

        #The two accelerometers are currently analog and are in the process of being switched out for digital ones.
        #The butter_lowpass_filter() function uses a digital filter. I am not sure how significant the difference using an analog filter will be,
        #but you can switch between the two by going to the butter_lowpass_filter() in Filter/filter.py, going to the line
        #"b, a = butter(order, normal_cutoff, btype="low", analog=False)," and changing analog to True.

        #self.data = filter.butter_lowpass_filter(self.data, name of the column as a str, non-normalized cutoff frequecy as a float, sampling frequency (fs) as a float, order as an int)
        self.data = filter.butter_lowpass_filter(self.data, "X", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(self.data, "Y", 4, 30, 2)
        self.data = filter.butter_lowpass_filter(self.data, "Z", 4, 30, 2)

    def convert_voltage_to_meters_per_sec_squared(self):
        constants = conversion_factor_enum.Constants
        for i, row in self.data.iterrows():
            #Each voltage reading in each axes first has the zero G voltage (1.5 V) subtracted from it. Then it is multiplied by the sensitivity factor (0.3 V/G), so that the product
            #is in Gs of acceleration. Then, the Gs are converted to m/s^2.
            self.data.loc[i, "X"] = (row["X"] - ANALOG_ACCEL_CONVERSION_OFFSET) / ANALOG_ACCEL_CONVERSION_CONSTANT * Gs_TO_METERS_PER_SEC_SQUARED_CONVERSION_FACTOR
            self.data.loc[i, "Y"] = (row["Y"] - ANALOG_ACCEL_CONVERSION_OFFSET) / ANALOG_ACCEL_CONVERSION_CONSTANT * Gs_TO_METERS_PER_SEC_SQUARED_CONVERSION_FACTOR
            self.data.loc[i, "Z"] = (row["Z"] - ANALOG_ACCEL_CONVERSION_OFFSET) / ANALOG_ACCEL_CONVERSION_CONSTANT * Gs_TO_METERS_PER_SEC_SQUARED_CONVERSION_FACTOR
