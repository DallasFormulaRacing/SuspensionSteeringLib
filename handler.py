from conversions.conversions import Conversions
from calculations.calculations import Calculations
from plots.make_plot import make_plot
import traceback

conversions = Conversions("data\\output2_linpot_2023-10-14_13-23-28.csv")
calculations = Calculations("data\\output2_linpot_2023-10-14_13-23-28.csv")


class handler:

    def wheel_load_handler(self):
        # loads and prepares initial data
        conversions.convert_voltage_to_in()
        conversions.convert_time(conversions.data)
        conversions.clean_data()
        calculations.data = conversions.data

        # calculating constants
        calculations.calculate_wheel_rate_front()
        calculations.calculate_wheel_rate_rear()
        calculations.calculate_wheel_rate_roll_front()
        calculations.calculate_wheel_rate_roll_rear()
        calculations.calculate_K_H_K_P()
        calculations.calculate_K_R_K_W()
        calculations.calculate_a_b()
        calculations.calculate_q_w()

        # calculates wheel load formulas in pounds of force
        calculations.calculate_force_front_left()
        calculations.calculate_force_front_right()
        calculations.calculate_force_rear_left()
        calculations.calculate_force_rear_right()

        plots = make_plot(calculations.data)
        # plots.plot_wheel_load_vs_acceleration()
        plots.plot_wheel_load_vs_time()

    def wheel_damper_handler(self):
        # call the convert to mm method from conversions
        displacement_df = calculations.calculate_displacement()
        time_constant = calculations.calculate_time_constant()
        velocity_df = calculations.calculate_velocities(displacement_df, time_constant)
        print(velocity_df)


def main():
    handler_instance = handler()
    try:
        handler_instance.wheel_load_handler()
        handler_instance.wheel_damper_handler()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
