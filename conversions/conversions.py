import pandas as pd
from pandas import DataFrame
import plotly.express as px
import time
from sklearn.cluster import KMeans
from Filter import Filter
import Visualizer

SPRING_RATE_FRONT = 200.0 
SPRING_RATE_REAR = 175.0
MOTION_RATIO_FRONT = 0.907
MOTION_RATIO_REAR = 0.87
SPRING_RATE_ROLL_FRONT = 150.0 # guestimate Todo replace with real values
SPRING_RATE_ROLL_REAR = 150.0 # guestimate Todo replace with real values
MOTION_RATIO_ROLL_FRONT = 0.9 # Estimate
MOTION_RATIO_ROLL_REAR = 0.9 # Estimate
CORNER_WEIGHT_LF = 150.0 
CORNER_WEIGHT_RF = 150.0
CORNER_WEIGHT_RL = 150.0
CORNER_WEIGHT_RR = 150.0

class conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701
    ACCEL_G_CONSTANT = 1.0
    FL_CORNER_WEIGHT = 150.0
    FR_CORNER_WEIGHT = 150.0
    RL_CORNER_WEIGHT = 150.0
    RR_CORNER_WEIGHT = 150.0


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

    def convert_voltage_to_in(self):
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = (-(row["Front Right"] * 15.0) + 75.0) * 0.0393701
            self.data.loc[i, "Front Left"] = (-(row["Front Left"] * 15.0) + 75.0) * 0.0393701
            self.data.loc[i, "Rear Right"] = (-(row["Rear Right"] * 15.0) + 75.0) * 0.0393701
            self.data.loc[i, "Rear Left"] = (-(row["Rear Left"] * 15.0) + 75.0) * 0.0393701

    def clean_data(self):
        self.data = Filter.Filter.butter_lowpass_filter(self.data, "Front Right", 4, 30, 2)
        self.data = Filter.Filter.butter_lowpass_filter(self.data, "Front Left", 4, 30, 2)
        self.data = Filter.Filter.butter_lowpass_filter(self.data, "Rear Right", 4, 30, 2)
        self.data = Filter.Filter.butter_lowpass_filter(self.data, "Rear Left", 4, 30, 2)

    def calculate_wheeel_ratio_front(self) -> float:
     self.wheel_ratio_front = (SPRING_RATE_FRONT)/(MOTION_RATIO_FRONT ** 2)
     return self.wheel_ratio_front
   
    def calculate_wheel_ratio_rear(self) -> float:
     self.wheel_ratio_rear = (SPRING_RATE_REAR)/(MOTION_RATIO_REAR ** 2)
     return self.wheel_ratio_rear
   
    def calculate_wheel_ratio_roll_front(self) -> float:
     self.wheel_ratio_roll_front = (SPRING_RATE_ROLL_FRONT)/(MOTION_RATIO_ROLL_FRONT ** 2)
     return self.wheel_ratio_roll_front
   
    def calculate_wheel_ratio_roll_rear(self) -> float:
     self.wheel_ratio_roll_rear = (SPRING_RATE_ROLL_REAR)/(MOTION_RATIO_ROLL_REAR ** 2)
     return self.wheel_ratio_roll_rear
   
    def calculate_K_H_K_P(self) -> float:
     self.K_H = 0.5 * ( self.wheel_ratio_front + self.wheel_ratio_rear )
     self.K_P = self.K_H
     return self.K_H
   
    def calculate_K_R_K_W(self) -> float:
     self.K_R = 0.5 * ( self.wheel_ratio_front + 2 * self.wheel_ratio_roll_front) + 0.5 * ( self.wheel_ratio_rear + 2 * self.wheel_ratio_roll_rear)
     self.K_W = self.K_R
     return self.K_R
   
    def calculate_a_b(self) -> float:
      self.wheel_load_const_a = 0.5 * ( self.wheel_ratio_front + 2 * self.wheel_ratio_roll_front) - 0.5 * ( self.wheel_ratio_rear + 2 * self.wheel_ratio_roll_rear)
      self.wheel_load_const_b = self.wheel_load_const_a
      return self.wheel_load_const_a
   
    def calculate_q_w(self) -> float:
     self.q = (self.K_R + self.wheel_load_const_a) / (self.K_R - self.wheel_load_const_a) - 1
     self.w = self.q
     return self.q
    
    def calculate_force_equations(self):
        self.Force_LF = CORNER_WEIGHT_LF + 0.25 * ( self.K_H * ( self.data["Front Left"] + self.data["Right Front"] + self.data["Rear left"] + self.data["Rear Right"]) + self.K_P * (self.data["Front Left"] + self.data["Right Front"] - self.data["Rear left"] - self.data["Rear Right"]) + self.K_R * ( self.data["Front Left"] - self.data["Right Front"] + self.data["Rear left"] - self.data["Rear Right"]) * self.q + self.K_W * ( self.data["Front Left"] - self.data["Right Front"] - self.data["Rear left"] + self.data["Rear Right"]) * (1 - self.w)) 
        self.Force_RF = CORNER_WEIGHT_RF + 0.25 * ( self.K_H * ( self.data["Front Left"] + self.data["Right Front"] + self.data["Rear left"] + self.data["Rear Right"]) + self.K_P * (self.data["Front Left"] + self.data["Right Front"] - self.data["Rear left"] - self.data["Rear Right"]) - self.K_R * ( self.data["Front Left"] - self.data["Right Front"] + self.data["Rear left"] - self.data["Rear Right"]) * self.q - self.K_W * ( self.data["Front Left"] - self.data["Right Front"] - self.data["Rear left"] + self.data["Rear Right"]) * (1 - self.w)) 
        self.Force_RR = CORNER_WEIGHT_RR + 0.25 * ( self.K_H * ( self.data["Front Left"] + self.data["Right Front"] + self.data["Rear left"] + self.data["Rear Right"]) - self.K_P * (self.data["Front Left"] + self.data["Right Front"] - self.data["Rear left"] - self.data["Rear Right"]) + self.K_R * ( self.data["Front Left"] - self.data["Right Front"] + self.data["Rear left"] - self.data["Rear Right"]) * (1 - self.q) - self.K_W * ( self.data["Front Left"] - self.data["Right Front"] - self.data["Rear left"] + self.data["Rear Right"]) * self.w)
        self.Force_LR = CORNER_WEIGHT_RL + 0.25 * ( self.K_H * ( self.data["Front Left"] + self.data["Right Front"] + self.data["Rear left"] + self.data["Rear Right"]) - self.K_P * (self.data["Front Left"] + self.data["Right Front"] - self.data["Rear left"] - self.data["Rear Right"]) - self.K_R * ( self.data["Front Left"] - self.data["Right Front"] + self.data["Rear left"] - self.data["Rear Right"]) * (1 - self.q) + self.K_W * ( self.data["Front Left"] - self.data["Right Front"] - self.data["Rear left"] + self.data["Rear Right"])  * self.w)
        return [self.Force_LF, self.Force_RF, self.Force_RR, self.Force_LR]
    
    def convert_to_gs(self) -> DataFrame:
        # convert the voltage to gs
        pass

    def convert_voltage_to_mm(self) -> DataFrame:
        pass
   
    def convert_time(self, data):
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )