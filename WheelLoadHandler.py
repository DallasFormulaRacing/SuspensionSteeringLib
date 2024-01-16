# Todo: change to handler.py and Code for conversions and calculations is currently in conversion_equations/conversions.py
import pandas as pd
import Visualizer
import make_plot

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

class WheelLoad:
   def __init__(self, filename: str ):
        self.filename = filename
        self.df = pd.DataFrame(pd.read_csv(filename))
        print(self.df)
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
   
   def calculate_consts(self) -> list:
        self.WR_F = (SPRING_RATE_FRONT)/(MOTION_RATIO_FRONT ** 2)
        self.WR_R = (SPRING_RATE_REAR)/(MOTION_RATIO_REAR ** 2)
        self.WR_Rollf = (SPRING_RATE_Roll_front) / (MOTION_RATIO_Roll_front ** 2)
        self.WR_Rollr = (SPRING_RATE_Roll_rear) / (MOTION_RATIO_Roll_rear ** 2)
        self.K_H = 0.5 * ( self.WR_F + self.WR_R)
        self.K_P = self.K_H
        self.K_R = 0.5 * ( self.WR_F + 2 * self.WR_Rollf) + 0.5 * ( self.WR_R + 2 * self.WR_Rollr)
        self.K_W = self.K_R
        self.a = 0.5 * ( self.WR_F + 2 * self.WR_Rollf) - 0.5 * ( self.WR_R + 2 * self.WR_Rollr)
        self.b = self.a
        self.q = (self.K_R + self.a) / (self.K_R - self.a) -1
        self.w = self.q
        return [self.WR_F, self.WR_R, self.WR_Rollf, self.WR_Rollr, self.K_H, self.K_P, self.K_R, self.K_W, self.a, self.b, self.q, self.w]

   def calculate_force_equations(self):
        self.Force_LF = CORNER_WEIGHT_LF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
        self.Force_RF = CORNER_WEIGHT_RF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
        self.Force_RR = CORNER_WEIGHT_RR + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
        self.Force_LR = CORNER_WEIGHT_RL + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
        return [self.Force_LF, self.Force_RF, self.Force_RR, self.Force_LR]

   def plot_wheel_load_vs_acceleration(self):
        columns = [self.Force_LF, self.Force_RF, self.Force_RR, self.Force_LR, self.acceleration]
        Visualizer.Visualize.plot(columns)
        #return ""

if __name__== "__main__":
    WL = WheelLoad("data\output2_linpot_2023-10-14_13-23-28.csv")
    WL.calculate_consts()
    WL.calculate_force_equations()
    make_plot.make_plot.plot_wheel_load_vs_time(WL)
    #make_plot.plot_wheel_load_vs_acceleration()