import pandas as pd
#imoport conversions class
from conversion_equations.conversions import Conversions

# create a conversions object from conversions class.

class handler:
    # import init method
    def __init__(self, file_name):
        self.conversions = Conversions(file_name)

    # method damper, utilize other methods and it should give velocities. 
    def process_damper_data(self):
        self.conversions.voltage_to_mm()
        time_const = self.conversions.cal_time_const()
        displacements = self.conversions.calc_displacements()
        velocities = self.conversions.calculate_velocity(displacements, time_const)
        damping_forces = self.conversions.estimate_damping_force(velocities, self.DAMPING_COEFFICIENT)
