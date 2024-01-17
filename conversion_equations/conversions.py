import pandas as pd
import numpy as np
import mpmath
from sympy import symbols, diff

class conversions:
    linpot_fr_conversion_factor = 15.0
    linpot_fl_conversion_factor = 15.0
    linpot_rr_conversion_factor = 15.0
    linpot_rl_conversion_factor = 15.0

    def __init__(self) -> None:
        # read in the data files
        self.linpot_file_name = "output2_linpot_2023-10-14_13-23-28.csv"
        self.linpot_data = pd.DataFrame(pd.read_csv(self.linpot_file_name))

        self.acc_file_name = "output2_analog_2023-10-14_13-18-15.csv"
        self.acc_data = pd.DataFrame(pd.read_csv(self.acc_file_name))

        self.fr_basis = self.linpot_data.loc[0,"Front Right"]
        self.fl_basis = self.linpot_data.loc[0,"Front Left"]
        self.rr_basis = self.linpot_data.loc[0,"Rear Right"]
        self.rl_basis = self.linpot_data.loc[0,"Rear Left"]

        self.x_basis = self.acc_data.loc[0,"X"]
        self.y_basis = self.acc_data.loc[0,"Y"]
        self.z_basis = self.acc_data.loc[0,"Z"]


    
    def voltage_to_mm(self, column_name: str) -> None:
        # Check if the column exists in the DataFrame
        if column_name in self.data.columns:
            self.data[column_name] = self.data[column_name] * self.linpot_fr_conversion_factor
        else:
            print(f"Column '{column_name}' not found in the DataFrame.")
    


    def calculate_velocity(accelerations, time_intervals):
        """
        Calculate velocity from acceleration data.
        :param accelerations: DataFrame of acceleration values.
        :param time_intervals: DataFrame column for time values.
        :return: List of velocity values. """

        velocities = [0]  # starting with an initial velocity of 0
        for i in range(1, len(accelerations)):
            # Velocity = Previous Velocity + (Acceleration * Time Interval)
            velocity = velocities[i-1] + accelerations[i] * time_intervals[i]
            velocities.append(velocity)
        return velocities

    accelerations = [0.5, 0.6, 0.55, 0.4, 0.3]  # Accelerations in m/s^2
    time_stamps = [0, 1, 2, 3, 4]  # Time stamps in seconds

    time_intervals = np.diff(time_stamps)

    velocities = calculate_velocity(accelerations, time_intervals)

    print("Velocities:", velocities)



    def calculate_velocity(displacements, time_stamps):
        """
        Another method of calculating velocity from displacement data.
        :param displacements: List or array of displacement values. Displacement values will need to be calculated for this to work, this will be the difference in position between the starting point and its positions at each interval, this will also need to be a new DF
        :param time_stamps: List or array of time stamps.
        :return: List of velocity values.
        """
        velocities = []
        for i in range(1, len(displacements)):
            delta_x = displacements[i] - displacements[i - 1]
            delta_t = time_stamps[i] - time_stamps[i - 1]
            velocity = delta_x / delta_t
            velocities.append(velocity)
        return velocities

    def estimate_damping_force(velocities, damping_coefficient):
        """
        Estimate the damping force using the damping coefficient and velocity.

        :param velocities: List or array of velocity values.
        :param damping_coefficient: Damping coefficient (constant).
        :return: List of estimated damping forces.
        """
        damping_forces = [damping_coefficient * v for v in velocities]
        return damping_forces

            



    # displacement in mm and time in seconds
    def get_velocity_from_displacements_times(self, displacement1, displacement2, time1, time2):
        return (displacement2 - displacement1) / (time2 - time1)
    
    # acceleration in m/s^2 and time interval in seconds
    def get_velocity_from_acceleration_time(self, acceleration, time_interval):
        return acceleration * time_interval
    

    # method for converting g's to m/s^2
    def g_to_meters_per_second(self, g):
        return g * 9.82
    
    # mass in kg and acceleration in m/s^2
    def get_force(self, mass, acceleration):
        return mass * acceleration
    
    # get acceleration from velocity
    def get_acceleration(self,velocity):
        t = symbols('t')
        acceleration = diff(velocity, t)
        return acceleration

    
