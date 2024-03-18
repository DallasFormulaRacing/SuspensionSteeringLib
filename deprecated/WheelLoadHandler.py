import pandas as pd
import deprecated.Visualizer as Visualizer
import deprecated.make_plot as make_plot

SPRING_RATE_FRONT = 200.0
SPRING_RATE_REAR = 175.0
MOTION_RATIO_FRONT = 0.907
MOTION_RATIO_REAR = 0.87
SPRING_RATE_ROLL_FRONT = 150.0  # guestimate Todo replace with real values
SPRING_RATE_ROLL_REAR = 150.0  # guestimate Todo replace with real values
MOTION_RATIO_ROLL_FRONT = 0.9  # Estimate
MOTION_RATIO_ROLL_REAR = 0.9  # Estimate
CORNER_WEIGHT_LF = 150.0
CORNER_WEIGHT_RF = 150.0
CORNER_WEIGHT_RL = 150.0
CORNER_WEIGHT_RR = 150.0


class WheelLoad:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = pd.DataFrame(pd.read_csv(self.filename))
        self.switch_columns()

    def switch_columns(self):
        self.data = self.data.rename(
            columns={
                "Front Right": "Front Left",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
            }
        )

    def convert_voltage_to_mm(self):
        for i, row in self.data.iterrows():
            self.data.loc[i, "Front Right"] = -(row["Front Right"] * 15.0) + 75.0
            self.data.loc[i, "Front Left"] = -(row["Front Left"] * 15.0) + 75.0
            self.data.loc[i, "Rear Right"] = -(row["Rear Right"] * 15.0) + 75.0
            self.data.loc[i, "Rear Left"] = -(row["Rear Left"] * 15.0) + 75.0

    def calculate_wheeel_ratio_front(self) -> float:
        self.wheel_ratio_front = (SPRING_RATE_FRONT)/(MOTION_RATIO_FRONT ** 2)
        return self.wheel_ratio_front

    def calculate_wheel_ratio_rear(self) -> float:
        self.wheel_ratio_rear = (SPRING_RATE_REAR)/(MOTION_RATIO_REAR ** 2)
        return self.wheel_ratio_rear

    def calculate_wheel_ratio_Rollf(self) -> float:
        self.wheel_ratio_roll_front = (SPRING_RATE_ROLL_FRONT)/(MOTION_RATIO_ROLL_FRONT ** 2)
        return self.wheel_ratio_roll_front

    def calculate_wheel_ratio_Rollr(self) -> float:
        self.wheel_ratio_roll_rear = (SPRING_RATE_ROLL_REAR)/(MOTION_RATIO_ROLL_REAR ** 2)
        return self.wheel_ratio_roll_rear

    def calculate_K_H_K_P(self) -> float:
        self.K_H = 0.5 * (self.wheel_ratio_front + self.wheel_ratio_rear)
        self.K_P = self.K_H
        return self.K_H

    def calculate_K_R_K_W(self) -> float:
        self.K_R = 0.5 * (self.wheel_ratio_front + 2 * self.wheel_ratio_roll_front) + \
            0.5 * (self.wheel_ratio_rear + 2 * self.wheel_ratio_Roll_rear)
        self.K_W = self.K_R
        return self.K_R

    def calculate_a_b(self) -> float:
        self.wheel_load_const_a = 0.5 * (self.wheel_ratio_front + 2 * self.wheel_ratio_Roll_front) - \
            0.5 * (self.wheel_ratio_rear + 2 * self.wheel_ratio_Roll_rear)
        self.wheel_load_const_b = self.wheel_load_const_a
        return self.wheel_load_const_a

    def calculate_q_w(self) -> float:
        self.q = (self.K_R + self.a) / (self.K_R - self.a) - 1
        self.w = self.q
        return self.q

    def calculate_consts(self) -> list:
        self.WR_F = (SPRING_RATE_FRONT)/(MOTION_RATIO_FRONT ** 2)
        self.WR_R = (SPRING_RATE_REAR)/(MOTION_RATIO_REAR ** 2)
        self.WR_Rollf = (SPRING_RATE_ROLL_FRONT) / (MOTION_RATIO_ROLL_FRONT ** 2)
        self.WR_Rollr = (SPRING_RATE_ROLL_REAR) / (MOTION_RATIO_ROLL_REAR ** 2)
        self.K_H = 0.5 * (self.WR_F + self.WR_R)
        self.K_P = self.K_H
        self.K_R = 0.5 * (self.WR_F + 2 * self.WR_Rollf) + 0.5 * (self.WR_R + 2 * self.WR_Rollr)
        self.K_W = self.K_R
        self.a = 0.5 * (self.WR_F + 2 * self.WR_Rollf) - 0.5 * (self.WR_R + 2 * self.WR_Rollr)
        self.b = self.a
        self.q = (self.K_R + self.a) / (self.K_R - self.a) - 1
        self.w = self.q
        return [self.WR_F, self.WR_R, self.WR_Rollf, self.WR_Rollr, self.K_H, self.K_P, self.K_R, self.K_W, self.a, self.b, self.q, self.w]

    def calculate_force_equations(self):
        self.data["Force_LF"] = CORNER_WEIGHT_LF + 0.25 * (self.K_H * (self.data["Front Left"] + self.data["Front Right"] + self.data["Rear Left"] + self.data["Rear Right"]) + self.K_P * (self.data["Front Left"] + self.data["Front Right"] - self.data["Rear Left"] - self.data["Rear Right"]) + self.K_R * (
            self.data["Front Left"] - self.data["Front Right"] + self.data["Rear Left"] - self.data["Rear Right"]) * self.q + self.K_W * (self.data["Front Left"] - self.data["Front Right"] - self.data["Rear Left"] + self.data["Rear Right"]) * (1 - self.w))
        self.data["Force_RF"] = CORNER_WEIGHT_RF + 0.25 * (self.K_H * (self.data["Front Left"] + self.data["Front Right"] + self.data["Rear Left"] + self.data["Rear Right"]) + self.K_P * (self.data["Front Left"] + self.data["Front Right"] - self.data["Rear Left"] - self.data["Rear Right"]) - self.K_R * (
            self.data["Front Left"] - self.data["Front Right"] + self.data["Rear Left"] - self.data["Rear Right"]) * self.q - self.K_W * (self.data["Front Left"] - self.data["Front Right"] - self.data["Rear Left"] + self.data["Rear Right"]) * (1 - self.w))
        self.data["Force_RR"] = CORNER_WEIGHT_RR + 0.25 * (self.K_H * (self.data["Front Left"] + self.data["Front Right"] + self.data["Rear Left"] + self.data["Rear Right"]) - self.K_P * (self.data["Front Left"] + self.data["Front Right"] - self.data["Rear Left"] - self.data["Rear Right"]) + self.K_R * (
            self.data["Front Left"] - self.data["Front Right"] + self.data["Rear Left"] - self.data["Rear Right"]) * (1 - self.q) - self.K_W * (self.data["Front Left"] - self.data["Front Right"] - self.data["Rear Left"] + self.data["Rear Right"]) * self.w)
        self.data["Force_LR"] = CORNER_WEIGHT_RL + 0.25 * (self.K_H * (self.data["Front Left"] + self.data["Front Right"] + self.data["Rear Left"] + self.data["Rear Right"]) - self.K_P * (self.data["Front Left"] + self.data["Front Right"] - self.data["Rear Left"] - self.data["Rear Right"]) - self.K_R * (
            self.data["Front Left"] - self.data["Front Right"] + self.data["Rear Left"] - self.data["Rear Right"]) * (1 - self.q) + self.K_W * (self.data["Front Left"] - self.data["Front Right"] - self.data["Rear Left"] + self.data["Rear Right"]) * self.w)
        return [self.data["Force_LF"], self.data["Force_RF"], self.data["Force_RR"], self.data["Force_LR"]]

    def plot_wheel_load_vs_acceleration(self):
        columns = [self.data["Force_LF"], self.data["Force_RF"], self.data["Force_RR"], self.data["Force_LR"], self.data["acceleration"]]
        Visualizer.Visualize.plot(columns)

    def plot_wheel_load_vs_time(self):
        columns = [self.data["Force_LF"], self.data["Force_RF"], self.data["Force_RR"], self.data["Force_LR"], self.data["time"]]
        Visualizer.Visualize.plot(columns)


if __name__ == "__main__":
    WL = WheelLoad("data\output2_linpot_2023-10-14_13-23-28.csv")
    WL.calculate_consts()
    WL.calculate_force_equations()
    make_plot.make_plot.plot_wheel_load_vs_time(WL)
    # make_plot.plot_wheel_load_vs_acceleration()
