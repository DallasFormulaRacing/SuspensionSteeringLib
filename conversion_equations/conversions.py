import pandas as pd
from pandas import DataFrame
import plotly.express as px
import time
from sklearn.cluster import KMeans
from Filter import Filter
import Visualizer

SR_F = 200.0 
SR_R = 175.0
MR_F = 0.907
MR_R = 0.87
SR_Rollf = 150.0 # guestimate Todo replace with real values
SR_Rollr = 150.0 # guestimate Todo replace with real values
MR_Rollf = 0.9 # Estimate
MR_Rollr = 0.9 # Estimate
W_LF = 150.0 
W_RF = 150.0
W_RL = 150.0
W_RR = 150.0

SPRING_RATE_FRONT = 200.0 
SPRING_RATE_REAR = 175.0
MOTION_RATIO_FRONT = 0.907
MOTION_RATIO_REAR = 0.87
SPRING_RATE_Roll_front = 150.0 # guestimate Todo replace with real values
SPRING_RATE_Roll_rear = 150.0 # guestimate Todo replace with real values
MOTION_RATIO_Roll_front = 0.9 # Estimate
MOTION_RATIO_Roll_rear = 0.9 # Estimate
CORNER_WEIGHT_LF = 150.0 
CORNER_WEIGHT_RF = 150.0
CORNER_WEIGHT_RL = 150.0
CORNER_WEIGHT_RR = 150.0

class conversions:

    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    ACCEL_G_CONSTANT = 1.0
    FL_CORNER_WEIGHT = 150.0
    FR_CORNER_WEIGHT = 150.0
    RL_CORNER_WEIGHT = 150.0
    RR_CORNER_WEIGHT = 150.0


    def __init__(self, filename: str ):
        self.filename = filename
        self.df = pd.DataFrame(pd.read_csv(filename))

        #self.WR_F = 0.0
        #self.WR_R = 0.0
        #self.WR_Rollf = 0.0
        #self.WR_Rollr = 0.0
        #self.K_H = 0.0
        #self.K_P = 0.0
        #self.K_W = 0.0
        #self.K_R = 0.0
        #self.q = 0.0
        #self.w = 0.0


    def calculate_wheeel_ratio_front(self) -> float:
     self.wheel_ratio_front = (SPRING_RATE_FRONT)/(MOTION_RATIO_FRONT ** 2)
     return self.wheel_ratio_front
   
    def calculate_wheel_ratio_rear(self) -> float:
     self.wheel_ratio_rear = (SPRING_RATE_REAR)/(MOTION_RATIO_REAR ** 2)
     return self.wheel_ratio_rear
   
    def calculate_wheel_ratio_Rollf(self) -> float:
     self.wheel_ratio_Roll_front = (SPRING_RATE_Roll_front)/(MOTION_RATIO_Roll_front ** 2)
     return self.wheel_ratio_Roll_front
   
    def calculate_wheel_ratio_Rollr(self) -> float:
     self.wheel_ratio_Roll_rear = (SPRING_RATE_Roll_rear)/(MOTION_RATIO_Roll_rear ** 2)
     return self.wheel_ratio_Roll_rear
   
    def calculate_K_H_K_P(self) -> float:
     self.K_H = 0.5 * ( self.wheel_ratio_front + self.wheel_ratio_rear)
     self.K_P = self.K_H
     return self.K_H
   
    def calculate_K_R_K_W(self) -> float:
     self.K_R = 0.5 * ( self.wheel_ratio_front + 2 * self.wheel_ratio_Roll_front) + 0.5 * ( self.wheel_ratio_rear + 2 * self.wheel_ratio_Roll_rear)
     self.K_W = self.K_R
     return self.K_R
   
    def calculate_a_b(self) -> float:
      self.wheel_load_const_a = 0.5 * ( self.wheel_ratio_front + 2 * self.wheel_ratio_Roll_front) - 0.5 * ( self.wheel_ratio_rear + 2 * self.wheel_ratio_Roll_rear)
      self.wheel_load_const_b = self.wheel_load_const_a
      return self.wheel_load_const_a
   
    def calculate_q_w(self) -> float:
     self.q = (self.K_R + self.a) / (self.K_R - self.a) - 1
     self.w = self.q
     return self.q
   
    def calculate_forces_part_1(self) -> float:
       return 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR))
    
    def calculate_forces_part_2(self) -> float:
       self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR)
    
    def calculate_forces_part_3_front(self) -> float:
       self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q

    def calculate_forces_part_3_rear(self) -> float:
       self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q)

    def calculate_forces_part_4_front(self) -> float:
       self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)
    
    def calculate_forces_part_4_rear(self) -> float:
       (1 - self.q) - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w

    def calculate_force_front_left(self) -> float:
       self.Force_LF = CORNER_WEIGHT_LF + self.calculate_forces_part_1() + self.calculate_forces_part_2() + self.calculate_forces_part_3_front() + self.calculate_forces_part_4_front()
       return self.Force_LF
    
    def calculate_force_front_right(self) -> float:
       self.Force_RF = CORNER_WEIGHT_RF + self.calculate_forces_part_1() + self.calculate_forces_part_2() - self.calculate_forces_part_3_front() - self.calculate_forces_part_4_front()
       return self.Force_RF
    
    def calculate_force_rear_right(self) -> float:
       self.Force_RR = CORNER_WEIGHT_RF + self.calculate_forces_part_1() - self.calculate_forces_part_2() + self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear()
       return self.Force_RR
    
    def calculate_force_rear_left(self) -> float:
       self.Force_LR = CORNER_WEIGHT_RL + self.calculate_forces_part_1() - self.calculate_forces_part_2() - self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear()
       return self.Force_LR
    
    def calculate_force_equations(self):
        self.Force_LF = CORNER_WEIGHT_LF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
        self.Force_RF = CORNER_WEIGHT_RF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
        self.Force_RR = CORNER_WEIGHT_RR + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
        self.Force_LR = CORNER_WEIGHT_RL + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
        return [self.Force_LF, self.Force_RF, self.Force_RR, self.Force_LR]
    
    def plot_wheel_load_vs_acceleration(self):
        columns = columns[self.Force_LF, self.Force_RL, self.Force_RR, self.Force_LR, self.acceleration]
        Visualizer.Visualize.plot(columns)
        #return ""
    def __init__(self):
        pass

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



