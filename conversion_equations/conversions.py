import pandas as pd
import numpy as np
import time 

class Conversions:
    x_conversion_constant_pos = 0.50381
    x_conversion_constant_neg = -0.75487
    y_conversion_constant_pos = 0.51310
    y_conversion_constant_neg = -0.77434
    z_conversion_constant_pos = 0.49961
    z_conversion_constant_neg = -0.74178

    def __init__(self) -> None:
        self.file_name = "data/output2_analog_2023-10-14_13-18-15.csv"
        self.data = pd.DataFrame(pd.read_csv(self.file_name))
        self.x_basis = self.data.loc[0, "X"]
        self.y_basis = self.data.loc[0, "Y"]
        self.z_basis = self.data.loc[0, "Z"]

    def convert_time(self) -> None:
        for i, row in self.data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            self.data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )

    # convert voltage to g using conversion constants
    def convert_voltage_to_g(self) -> None:
        for i, row in self.data.iterrows():
            self.data.loc[i, "X"] = (row["X"] - self.x_basis) * self.x_conversion_constant_pos
            self.data.loc[i, "Y"] = (row["Y"] - self.y_basis) * self.y_conversion_constant_pos 
            self.data.loc[i, "Z"] = (row["Z"] - self.z_basis) * self.z_conversion_constant_pos

    # calculate the yaw rate by subtracting the Y-rear acceleration from the Y-front acceleration and dividing by the wheelbase
    def calculate_yaw(self, y_front_acc, y_rear_acc, wheelbase):
        yaw_rate = (y_front_acc - y_rear_acc) / wheelbase
        return yaw_rate 

    # calculate the predicted lateral acceleration using the cornering equation
    def calculate_cornering(self, yaw_rate, velocity):
        predicted_lat_acc = yaw_rate * velocity
        return predicted_lat_acc

    # calculate understeer and oversteer using the predicted lateral acceleration
    def calculate_understeer_oversteer(self, lat_acc, predicted_lat_acc):
        understeer_oversteer = lat_acc - predicted_lat_acc
        return understeer_oversteer

 





    
