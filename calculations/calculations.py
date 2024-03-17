import pandas as pd
from calculations.constant_enum import Constants as constants


class Calculations:

    def __init__(self, filename: str):
        self.linpot_dataframe = pd.DataFrame(pd.read_csv(filename))

    def calculate_displacement(self) -> pd.DataFrame:
        self.linpot_dataframe['Displacement Front Right'] = self.linpot_dataframe['Front Right'].diff(
        ).fillna(0)
        self.linpot_dataframe['Displacement Front Left'] = self.linpot_dataframe['Front Left'].diff(
        ).fillna(0)
        self.linpot_dataframe['Displacement Rear Right'] = self.linpot_dataframe['Rear Right'].diff(
        ).fillna(0)
        self.linpot_dataframe['Displacement Rear Left'] = self.linpot_dataframe['Rear Left'].diff(
        ).fillna(0)

        # self.linpot_dataframe.to_csv('fake_csv.csv')

        return self.linpot_dataframe

    # move over time method
    def calculate_time_constant(self) -> float:
        pass

    def calculate_velocities(self, displacements: pd.DataFrame, time_const: float) -> pd.DataFrame:
        # apply to each column you need to convert
        for i, row in self.linpot_dataframe.itterows():
            pass

    # put in math for finding velocity, return velocity
    def calculate_velocity(self) -> float:
        pass

    def calculate_wheel_loads(self, df: pd.DataFrame) -> pd.DataFrame:
        print(self.K_H)
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


def main():
    # Replace with your actual filename
    filename = 'data\\output2_linpot_2023-10-14_13-23-28.csv'
    calculations = Calculations(filename)
    df_with_displacement = calculations.calculate_displacement()
    print(df_with_displacement)


# Ensures that the main function is called only when this script is executed directly (not imported as a module)
if __name__ == '__main__':
    main()
