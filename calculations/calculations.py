
import numpy as np
import pandas as pd
from calculations.constants import Constants_23 as constants


class Calculations:

    def __init__(self, filename: str):
        self.linpot_dataframe = pd.DataFrame(pd.read_csv(filename))

    def calculate_displacement(self) -> pd.DataFrame:

        displacement_df = self.linpot_dataframe.copy()

        displacement_df['Displacement Front Right'] = self.linpot_dataframe['Front Right'].diff(
        ).fillna(0)
        displacement_df['Displacement Front Left'] = self.linpot_dataframe['Front Left'].diff(
        ).fillna(0)
        displacement_df['Displacement Rear Right'] = self.linpot_dataframe['Rear Right'].diff(
        ).fillna(0)
        displacement_df['Displacement Rear Left'] = self.linpot_dataframe['Rear Left'].diff(
        ).fillna(0)

        return displacement_df

    def calculate_time_constant(self) -> float:
        time_const = self.linpot_dataframe.loc[0, "Time"] - self.linpot_dataframe.loc[1, "Time"]
        return time_const

    def calculate_velocities(self) -> pd.DataFrame:

        displacement_df = self.calculate_displacement()

        print(displacement_df)

        for i, row in displacement_df.iterrows():
            displacement_df.loc[i, 'Velocity Front Right'] = self.calculate_velocity(
                row['Displacement Front Right'])
            displacement_df.loc[i, 'Velocity Front Left'] = self.calculate_velocity(
                row['Displacement Front Left'])
            displacement_df.loc[i, 'Velocity Rear Right'] = self.calculate_velocity(
                row['Displacement Rear Right'])
            displacement_df.loc[i, 'Velocity Rear Left'] = self.calculate_velocity(
                row['Displacement Rear Left'])

        return displacement_df

    def calculate_velocity(self, displacement: float) -> float:
        time_const = self.calculate_time_constant()
        return displacement / time_const

    def estimate_damping_force(self) -> pd.DataFrame:

        dampening_df = self.calculate_velocities()

        for i, row in dampening_df.iterrows():
            dampening_df.loc[i, 'Damping Force Front Right'] = -(row["Velocity Front Right"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Front Left'] = -(row["Velocity Front Left"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Rear Right'] = -(row["Velocity Rear Right"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Rear Left'] = -(row["Velocity Rear Left"] * constants.DAMPING_COEFFICIENT)

        return dampening_df

    def calculate_forces_part_1(self) -> float:
        return self.K_H * (self.data["Front Left_lowpass"] + self.data["Front Right_lowpass"] +
                           self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"])

    def calculate_forces_part_2(self) -> float:
        return self.K_P * (self.data["Front Left_lowpass"] + self.data["Front Right_lowpass"] -
                           self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"])

    def calculate_forces_part_3_front(self) -> float:
        return self.K_R * (self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] +
                           self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"]) * self.q

    def calculate_forces_part_3_rear(self) -> float:
        return self.K_R * (self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] +
                           self.data["Rear Left_lowpass"] - self.data["Rear Right_lowpass"]) * (1 - self.q)

    def calculate_forces_part_4_front(self) -> float:
        return self.K_W * (self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] -
                           self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"]) * (1 - self.w)

    def calculate_forces_part_4_rear(self) -> float:
        return self.K_W * (self.data["Front Left_lowpass"] - self.data["Front Right_lowpass"] -
                           self.data["Rear Left_lowpass"] + self.data["Rear Right_lowpass"]) * self.w

    def calculate_force_front_left(self) -> float:
        self.data["Force Front Left"] = constants.CORNER_WEIGHT_LF + 0.25 * (self.calculate_forces_part_1(
        ) + self.calculate_forces_part_2() + self.calculate_forces_part_3_front() + self.calculate_forces_part_4_front())
        return self.data["Force Front Left"]

    def calculate_force_front_right(self) -> float:
        self.data["Force Front Right"] = constants.CORNER_WEIGHT_RF + 0.25 * (self.calculate_forces_part_1(
        ) + self.calculate_forces_part_2() - self.calculate_forces_part_3_front() - self.calculate_forces_part_4_front())
        return self.data["Force Front Right"]

    def calculate_force_rear_right(self) -> float:
        self.data["Force Rear Right"] = constants.CORNER_WEIGHT_RR + 0.25 * (self.calculate_forces_part_1(
        ) - self.calculate_forces_part_2() + self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear())
        return self.data["Force Rear Right"]

    def calculate_force_rear_left(self) -> float:
        self.data["Force Rear Left"] = constants.CORNER_WEIGHT_RL + 0.25 * (self.calculate_forces_part_1(
        ) - self.calculate_forces_part_2() - self.calculate_forces_part_3_rear() - self.calculate_forces_part_4_rear())
        return self.data["Force Rear Left"]

    def calculate_wheel_rate_front(self) -> float:
        self.wheel_rate_front = (
            constants.SPRING_RATE_FRONT) / (constants.MOTION_RATIO_FRONT ** 2)
        return self.wheel_rate_front

    def calculate_wheel_rate_rear(self) -> float:
        self.wheel_rate_rear = (constants.SPRING_RATE_REAR) / \
                               (constants.MOTION_RATIO_REAR ** 2)
        return self.wheel_rate_rear

    def calculate_wheel_rate_roll_front(self) -> float:
        self.wheel_rate_roll_front = (
            constants.SPRING_RATE_ROLL_FRONT) / (constants.MOTION_RATIO_ROLL_FRONT ** 2)
        return self.wheel_rate_roll_front

    def calculate_wheel_rate_roll_rear(self) -> float:
        self.wheel_rate_roll_rear = (
            constants.SPRING_RATE_ROLL_REAR) / (constants.MOTION_RATIO_ROLL_REAR ** 2)
        return self.wheel_rate_roll_rear

    def calculate_K_H_K_P(self) -> float:
        self.K_H = 0.5 * (self.wheel_rate_front + self.wheel_rate_rear)
        self.K_P = self.K_H
        return self.K_H

    def calculate_K_R_K_W(self) -> float:
        self.K_R = 0.5 * (self.wheel_rate_front + 2 * self.wheel_rate_roll_front) + \
            0.5 * (self.wheel_rate_rear + 2 * self.wheel_rate_roll_rear)
        self.K_W = self.K_R
        return self.K_R

    def calculate_a_b(self) -> float:
        self.wheel_load_const_a = 0.5 * (self.wheel_rate_front + 2 * self.wheel_rate_roll_front) - 0.5 * (
            self.wheel_rate_rear + 2 * self.wheel_rate_roll_rear)
        self.wheel_load_const_b = self.wheel_load_const_a
        return self.wheel_load_const_a

    def calculate_q_w(self) -> float:
        self.q = ((self.K_R + self.wheel_load_const_a) /
                  (self.K_R - self.wheel_load_const_a)) - 1
        self.w = self.q
        return self.q

    @staticmethod
    def calculate_pitch_roll_angles(x, y, z) -> tuple[float, float]:
        # Calculate roll
        roll = np.arctan2(y, z) * 180 / np.pi

        # Calculate pitch
        pitch = np.arctan2(-x, np.sqrt(y * y + z * z)) * 180 / np.pi

        # Yaw is not directly calculable from accelerometer data

        return pitch, roll
