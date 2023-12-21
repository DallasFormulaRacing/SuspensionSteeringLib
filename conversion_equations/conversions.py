import pandas as pd
import plotly.express as px
import time
from sklearn.cluster import KMeans
from Filter import Filter

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

class conversions:
    x_conversion_const_pos = 0.50419
    linpot_const = 15.0
    
    
    def calculate_wheel_load_consts(self) -> list:
            self.WR_F = (SR_F)/(MR_F ** 2)
            self.WR_R = (SR_R)/(MR_R ** 2)
            self.WR_Rollf = (SR_Rollf) / (MR_Rollf ** 2)
            self.WR_Rollr = (SR_Rollr) / (MR_Rollr ** 2)
            self.K_H = 0.5 * ( self.WR_F + self.WR_R)
            self.K_P = self.K_H
            self.K_R = 0.5 * ( self.WR_F + 2 * self.WR_Rollf) + 0.5 * ( self.WR_R + 2 * self.WR_Rollr)
            self.K_W = self.K_R
            self.a = 0.5 * ( self.WR_F + 2 * self.WR_Rollf) - 0.5 * ( self.WR_R + 2 * self.WR_Rollr)
            self.b = self.a
            self.q = (self.K_R + self.a) / (self.K_R - self.a) -1
            self.w = self.q
            return [self.WR_F, self.WR_R, self.WR_Rollf, self.WR_Rollr, self.K_H, self.K_P, self.K_R, self.K_W, self.a, self.b, self.q, self.w]

    def calculate_wheel_load_force_equations(self):
            self.F_LF = W_LF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
            self.F_RF = W_RF + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) + self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * self.q - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * (1 - self.w)) 
            self.F_RR = W_RR + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) + self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) - self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
            self.F_LR = W_RR + 0.25 * ( self.K_H * ( self.displacement_LF + self.displacement_RF + self.displacement_RL + self.displacement_RR) - self.K_P * (self.displacement_LF + self.displacement_RF - self.displacement_RL - self.displacement_RR) - self.K_R * ( self.displacement_LF - self.displacement_RF + self.displacement_RL - self.displacement_RR) * (1 - self.q) + self.K_W * ( self.displacement_LF - self.displacement_RF - self.displacement_RL + self.displacement_RR) * self.w)
            return [self.F_LF, self.F_RF, self.F_RR, self.F_LR]

def convert_time(self, data):
        for i, row in data.iterrows():
            time_step = row["Time"]
            mlsec = repr(time_step).split(".")[1][:3]
            data.loc[i, "Time"] = time.strftime(
                "%H:%M:%S.{} %Z".format(mlsec), time.localtime(time_step)
            )



