from conversions.conversions import Conversions
from calculations.calculations import Calculations
from plots.make_plot import make_plot
import traceback

conversions = Conversions("data/output2_linpot_2023-10-14_13-23-28.csv", "data/output2_analog_2023-10-14_13-18-15.csv")
calculations = Calculations("data/output2_linpot_2023-10-14_13-23-28.csv")


class Client:

    def wheel_load_client(self):
        # loads and prepares initial data
        conversions.convert_voltage_to_in()
        conversions.convert_time(conversions.linpot_data)
        conversions.clean_linpot_data()
        calculations.data = conversions.linpot_data

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

    def wheel_damper_client(self):
        # call the convert to mm method from conversions
        displacement_df = calculations.calculate_displacement()
        time_constant = calculations.calculate_time_constant()
        velocity_df = calculations.calculate_velocities(displacement_df, time_constant)
        print(velocity_df)

    def linpot_conversion_client(self):
        conversions.clean_linpot_data()
        conversions.convert_voltage_to_mm()
        plots = make_plot(conversions.linpot_data)
        plots.plot_linpot_vs_time()

    def accel_conversion_client(self):
        conversions.convert_acel_to_g()
        conversions.convert_time(conversions.acel_data)
        plots = make_plot(conversions.acel_data)
        plots.plot_accel_vs_time()

    def pitch_roll_handler(self):
        x_y_z_low_pass_data = conversions.clean_acel_data()
        pitch_roll = conversions.generate_pitch_roll_df(x_y_z_low_pass_data)
        plots = make_plot(pitch_roll)
        plots.plot_pitch_roll_vs_time()


def main():
    handler_instance = Client()
    try:
        # handler_instance.wheel_load_handler()
        # handler_instance.linpot_handler()
        # handler_instance.accel_handler()
        handler_instance.pitch_roll_handler()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
