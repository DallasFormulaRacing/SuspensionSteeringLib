from conversions.conversions import Conversions
from calculations.calculations import Calculations
from plots.make_plot import make_plot
import traceback

conversions = Conversions("data/output2_linpot_2023-10-14_13-23-28.csv", "data/output2_analog_2023-10-14_13-18-15.csv")
calculations = Calculations("data/output2_linpot_2023-10-14_13-23-28.csv")

# TODO fix the filters


class Client:

    # Ofek rewrite this method
    def wheel_load_client(self):
        pass

    # Ofek rewrite this method
    def wheel_load_vs_acceleration_client(self):
        pass

    def damper_velocity_vs_time_client(self):
        velocity_df = calculations.calculate_velocities()
        plots = make_plot(velocity_df)
        fig = plots.plot_wheel_velocity_vs_time()
        fig.show()

    def damper_force_vs_time_client(self):
        dampening_force_df = calculations.estimate_damping_force()
        plots = make_plot(dampening_force_df)
        fig = plots.plot_damper_force_vs_velocity()
        fig.show()

    def linpot_vs_time_client(self):
        converted_data = conversions.convert_voltage_to_mm()
        plots = make_plot(converted_data)
        fig = plots.plot_linpot_vs_time()
        fig.show()

    def accel_vs_time_client(self):
        accel_g = conversions.convert_acel_to_g()
        print(accel_g)
        plots = make_plot(accel_g)
        fig = plots.plot_accel_vs_time()
        fig.show()

    def pitch_roll_client(self):
        x_y_z_low_pass_data = conversions.clean_acel_data()
        pitch_roll = conversions.generate_pitch_roll_df(x_y_z_low_pass_data)
        plots = make_plot(pitch_roll)
        fig = plots.plot_pitch_roll_vs_time()
        fig.show()


def main():
    client = Client()

    # conversions.clean_acel_data()
    # conversions.clean_linpot_data()

    try:
        client.damper_velocity_vs_time_client()
        client.damper_force_vs_time_client()
        client.wheel_load_client()
        client.linpot_vs_time_client()
        client.accel_vs_time_client()
        client.pitch_roll_client()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
