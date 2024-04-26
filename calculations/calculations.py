import numpy as np
import pandas as pd
from ..calculations.constants import Constants as constants


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

    def calculate_accelerations(self) -> pd.DataFrame:

        time_const = self.calculate_time_constant()
        accelerations_df = self.calculate_velocities()

        accelerations_df['Acceleration Front Right'] = accelerations_df['Velocity Front Right'].diff(
        ).fillna(0) / time_const
        accelerations_df['Acceleration Front Left'] = accelerations_df['Velocity Front Left'].diff(
        ).fillna(0) / time_const
        accelerations_df['Acceleration Rear Right'] = accelerations_df['Velocity Rear Right'].diff(
        ).fillna(0) / time_const
        accelerations_df['Acceleration Rear Left'] = accelerations_df['Velocity Rear Left'].diff(
        ).fillna(0) / time_const
            
        return accelerations_df
    
    def estimate_damping_force(self) -> pd.DataFrame:

        dampening_df = self.calculate_velocities()

        for i, row in dampening_df.iterrows():
            dampening_df.loc[i, 'Damping Force Front Right'] = -(row["Velocity Front Right"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Front Left'] = -(row["Velocity Front Left"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Rear Right'] = -(row["Velocity Rear Right"] * constants.DAMPING_COEFFICIENT)
            dampening_df.loc[i, 'Damping Force Rear Left'] = -(row["Velocity Rear Left"] * constants.DAMPING_COEFFICIENT)

        return dampening_df
    
    def calculate_wheel_loads(self, df: pd.DataFrame) -> pd.DataFrame:
        df_after_front_left = self.calculate_force_front_left(df)
        df_after_front_right = self.calculate_force_front_right(df_after_front_left)
        df_after_rear_left = self.calculate_force_rear_left(df_after_front_right)
        return self.calculate_force_rear_right(df_after_rear_left)

    def calculate_wheel_load_constants(self):
        self.calculate_wheel_rate_front()
        self.calculate_wheel_rate_rear()
        self.calculate_wheel_rate_roll_front()
        self.calculate_wheel_rate_roll_rear()
        self.calculate_K_H_K_P()
        self.calculate_K_R_K_W()
        self.calculate_a_b()
        self.calculate_q_w()

    def calculate_forces_part_1(self, df: pd.DataFrame) -> float:
        return self.K_H * (df["Front Left_lowpass"] + df["Front Right_lowpass"] +
                           df["Rear Left_lowpass"] + df["Rear Right_lowpass"])

    def calculate_forces_part_2(self, df: pd.DataFrame) -> float:
        return self.K_P * (df["Front Left_lowpass"] + df["Front Right_lowpass"] -
                           df["Rear Left_lowpass"] - df["Rear Right_lowpass"])

    def calculate_forces_part_3_front(self, df: pd.DataFrame) -> float:
        return self.K_R * (df["Front Left_lowpass"] - df["Front Right_lowpass"] +
                           df["Rear Left_lowpass"] - df["Rear Right_lowpass"]) * self.q

    def calculate_forces_part_3_rear(self, df: pd.DataFrame) -> float:
        return self.K_R * (df["Front Left_lowpass"] - df["Front Right_lowpass"] +
                           df["Rear Left_lowpass"] - df["Rear Right_lowpass"]) * (1 - self.q)

    def calculate_forces_part_4_front(self, df: pd.DataFrame) -> float:
        return self.K_W * (df["Front Left_lowpass"] - df["Front Right_lowpass"] -
                           df["Rear Left_lowpass"] + df["Rear Right_lowpass"]) * (1 - self.w)

    def calculate_forces_part_4_rear(self, df: pd.DataFrame) -> float:
        return self.K_W * (df["Front Left_lowpass"] - df["Front Right_lowpass"] -
                           df["Rear Left_lowpass"] + df["Rear Right_lowpass"]) * self.w

    def calculate_force_front_left(self, df) -> pd.DataFrame:
        df["Force Front Left"] = constants.CORNER_WEIGHT_LF + 0.25 * (self.calculate_forces_part_1(df
        ) + self.calculate_forces_part_2(df) + self.calculate_forces_part_3_front(df) + self.calculate_forces_part_4_front(df))
        return df

    def calculate_force_front_right(self, df) -> pd.DataFrame:
        df["Force Front Right"] = constants.CORNER_WEIGHT_RF + 0.25 * (self.calculate_forces_part_1(df
        ) + self.calculate_forces_part_2(df) - self.calculate_forces_part_3_front(df) - self.calculate_forces_part_4_front(df))
        return df

    def calculate_force_rear_right(self, df) -> pd.DataFrame:
        df["Force Rear Right"] = constants.CORNER_WEIGHT_RR + 0.25 * (self.calculate_forces_part_1(df
        ) - self.calculate_forces_part_2(df) + self.calculate_forces_part_3_rear(df) - self.calculate_forces_part_4_rear(df))
        return df

    def calculate_force_rear_left(self, df) -> pd.DataFrame:
        df["Force Rear Left"] = constants.CORNER_WEIGHT_RL + 0.25 * (self.calculate_forces_part_1(df
        ) - self.calculate_forces_part_2(df) - self.calculate_forces_part_3_rear(df) - self.calculate_forces_part_4_rear(df))
        return df

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


def main():
    # Replace with your actual filename
    filename = 'data\\output2_linpot_2023-10-14_13-23-28.csv'
    calculations = Calculations(filename)
    df_with_displacement = calculations.calculate_displacement()
    print(df_with_displacement)


# Ensures that the main function is called only when this script is executed directly (not imported as a module)
if __name__ == '__main__':
    main()
