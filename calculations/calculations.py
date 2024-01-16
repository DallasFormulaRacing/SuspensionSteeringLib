import pandas as pd
from pandas import DataFrame
import plotly.express as px
import time
from sklearn.cluster import KMeans
from Filter import Filter
import Visualizer

CORNER_WEIGHT_LF = 150.0 
CORNER_WEIGHT_RF = 150.0
CORNER_WEIGHT_RL = 150.0
CORNER_WEIGHT_RR = 150.0

class calculations:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = pd.DataFrame(pd.read_csv(filename))
        self.switch_columns()

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
   
    def convert_time(self, data):
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )
    
    def calculate_forces_part_1(self) -> float:
       return 0.25 * ( self.K_H * ( self.data["Front Left_lowpass"] + self.data["Front Right_lowpass"] + self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"]))
    
    def calculate_forces_part_2(self) -> float:
       return self.K_P * ( self.data["Front Left_lowpass"] + self.data["Front Right_lowpass"] - self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"])
      
    def calculate_forces_part_3_front(self) -> float:
       return self.K_R * ( self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] + self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"]) * self.q

    def calculate_forces_part_3_rear(self) -> float:
       return self.K_R * ( self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] + self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"]) * (1 - self.q)

    def calculate_forces_part_4_front(self) -> float:
       return self.K_W * ( self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] - self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"]) * (1 - self.w)
    
    def calculate_forces_part_4_rear(self) -> float:
       return self.K_W * ( self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] - self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"]) * self.w

    def calculate_force_front_left(self) -> float:
       self.data["Force Front Left (lbs)"] = CORNER_WEIGHT_LF + self.calculate_forces_part_1() + self.calculate_forces_part_2() + self.calculate_forces_part_3_front() + self.calculate_forces_part_4_front()
       return self.data["Force Front Left (lbs)"]
    
    def calculate_force_front_right(self) -> float:
       self.data["Force Front Right (lbs)"] = CORNER_WEIGHT_RF + self.calculate_forces_part_1() + self.calculate_forces_part_2() - self.calculate_forces_part_3_front() - self.calculate_forces_part_4_front()
       return self.data["Force Front Right (lbs)"]
    
    def calculate_force_rear_right(self) -> float:
       self.data["Force Rear Right (lbs)"] = CORNER_WEIGHT_RR + self.calculate_forces_part_1() - self.calculate_forces_part_2() + self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear()
       return self.data["Force Rear Right (lbs)"]
    
    def calculate_force_rear_left(self) -> float:
       self.data["Force Rear Left (lbs)"] = CORNER_WEIGHT_RL + self.calculate_forces_part_1() - self.calculate_forces_part_2() - self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear()
       return self.data["Force Rear Left (lbs)"]