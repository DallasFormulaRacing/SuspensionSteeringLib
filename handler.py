from conversions.conversions import Conversions
from calculations.calculations import Calculations
from plots import make_plot

conversions = Conversions("data\output2_linpot_2023-10-14_13-23-28.csv")
calculations = Calculations()
plots = make_plot.make_plot()


class handler:

    def wheel_load_handler():
        conversions.convert_voltage_to_in()
        conversions.convert_time(conversions.data)
        conversions.clean_data()
        calculations.data = conversions.data

        calculations.calculate_wheel_rate_front()
        calculations.calculate_wheel_rate_rear()
        calculations.calculate_wheel_rate_roll_front()
        calculations.calculate_wheel_rate_roll_rear()
        calculations.calculate_K_H_K_P()
        calculations.K_H
        calculations.calculate_K_R_K_W()
        calculations.K_W = calculations.K_R
        calculations.calculate_a_b()
        calculations.wheel_load_const_a
        calculations.calculate_q_w()
        calculations.w = calculations.q

        calculations.calculate_force_front_left()
        calculations.calculate_force_front_right()
        calculations.calculate_force_rear_left()
        calculations.calculate_force_rear_right()

        plots.plot_wheel_load_vs_time(calculations)

    def wheel_damper_handler():
        # call the convert to mm method from conversions
        displacement_df = calculations.calculate_displacement()
        time_constant = calculations.calculate_time_constant()
        velocity_df = calculations.calculate_velocities(displacement_df, time_constant)
