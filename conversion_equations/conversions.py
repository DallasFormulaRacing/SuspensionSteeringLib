import pandas as pd

class Conversions:
    LINPOT_CONVERSION_FACTOR = 15.0
    # dunno the damping coefficient yet, we need it
    DAMIPING_COEFFICIENT = 0

    def __init__(self, file_name : str):
        # create linpot_data datafram for linpot file
        self.file_name = file_name
        self.linpot_data = pd.DataFrame(pd.read_csv(self.linpot_file_name))

        # new data frame named displacements whhere the time column is removed, just displacements
        self.displacements = pd.DataFrame(pd.read_csv(self.linpot_file_name).drop("Time"), unit="s")


        self.fr_basis = self.linpot_data.loc[0,"Front Right"]
        self.fl_basis = self.linpot_data.loc[0,"Front Left"]
        self.rr_basis = self.linpot_data.loc[0,"Rear Right"]
        self.rl_basis = self.linpot_data.loc[0,"Rear Left"]


   # calculates voltage to mm using conversion factor.
        # reads row-wise first, then moves to the next row.
    def voltage_to_mm(self):
        for i, row in self.linpot_data.iterrows():
            self.linpot_data.loc[i, "Front Right"] = -(row["Front Right"] * self.LINPOT_CONVERSION_FACTOR) + 75.0
            self.linpot_data.loc[i, "Front Left"] = -(row["Front Left"] * self.LINPOT_CONVERSION_FACTOR) + 75.0
            self.linpot_data.loc[i, "Rear Right"] = -(row["Rear Right"] * self.LINPOT_CONVERSION_FACTOR) + 75.0
            self.linpot_data.loc[i, "Rear Left"] = -(row["Rear Left"] * self.LINPOT_CONVERSION_FACTOR) + 75.0


    # metod to calc. time constant, return time
    def cal_time_const(self):
        time_const = self.linpot_data.loc[0, "Time"] - self.linpot_data.loc[1, "Time"]
        return time_const


    # method to calculate displacement, returns a dataframe
        # reads column-wise first, then moves to the next column.
    def calc_displacements(self):
         # calculated displacemnt from resting displacement of linpot
        resting_displacement = self.displacements.head(4).mean()
        for i in range(0, len(self.displacements)):
            self.displacements.iloc[:, i] = self.displacements.iloc[:, i] - resting_displacement
        return self.displacements
    


    # Displacemnts is a dataFrame
    def calculate_velocity(self, displacements, time_const):
        """
        Another method of calculating velocity from displacement data.
        :param displacements: List or array of displacement values. Displacement values will need to be calculated for this to work, this will be the difference in position between the starting point and its positions at each interval, this will also need to be a new DF
        :param time_stamps: List or array of time stamps.
        :return: List of velocity values.
        """

        # FORMULA: Velociy = displacement / time_const

        # create a velocities array
        velocities = []

        # for the first row, displacement at the 1st calc. displacement is the delta between resing pos. and 1st reading. 
        velocity = self.displacements.iloc[0] / time_const
        velocities.append(velocity)

        # do this for all rows in the main dataframe
        for i in range(1, len(displacements)):
            delta_x = self.displacements.iloc[i] - self.displacements.iloc[i - 1]
            delta_t = time_const
            velocity = delta_x / delta_t
            velocities.append(velocity)
        return velocities
    


    # this is the force that will be on the damper
    # WHat is the DAMPING_COEFFICIENT? 
    def estimate_damping_force(velocities, DAMPING_COEFFICIENT):
        """
        Estimate the damping force using the damping coefficient and velocity.

        :param velocities: List or array of velocity values.
        :param DAMPING_COEFFICIENT: Damping coefficient (constant).
        :return: List of estimated damping forces.
        """
        damping_forces = [DAMPING_COEFFICIENT * v for v in velocities]
        return damping_forces

            




















"""


 # we need to find the force on the damper knowing the displacement
    def displacement_to_force(self):
         for i, row in self.data.iterrows():
            # Assuming you have a function or formula to calculate force based on displacement
            front_right_force = self.calculate_force(row["Front Right"])
            front_left_force = self.calculate_force(row["Front Left"])
            rear_right_force = self.calculate_force(row["Rear Right"])
            rear_left_force = self.calculate_force(row["Rear Left"])

            # Add the calculated forces to the DataFrame
            self.data.loc[i, "Damper Force"] = {
                "Front Right": front_right_force,
                "Front Left": front_left_force,
                "Rear Right": rear_right_force,
                "Rear Left": rear_left_force
            }
        # just add ot the data frame
         self.data.to_csv("./data/data/output2_linpot_2023-10-14_13-23-28.csv", index=False)


    def calculate_force(self, displacement):
        return displacement * 15










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

    
"""