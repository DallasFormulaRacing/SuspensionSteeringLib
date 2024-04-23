from .conversions.conversions import Conversions
from .calculations.calculations import Calculations
from .plots.make_plot import make_plot
import traceback
import pandas as pd

conversions = Conversions("./output2_linpot_2023-10-14_13-23-28.csv", "./output2_analog_2023-10-14_13-18-15.csv")
calculations = Calculations("./output2_linpot_2023-10-14_13-23-28.csv")
conversions.data_linpot = conversions.convert_time(conversions.data_linpot).copy()
#conversions.clean_data(conversions.data)


class client:
    def wheel_load_client(self):
        # loads and prepares initial data
        data_linpot = conversions.data_linpot.copy()
        data_linpot_converted = conversions.convert_voltage_to_in(data_linpot)
        df_cleaned = conversions.clean_data(data_linpot_converted)
        calculations.data = df_cleaned
        calculations.calculate_wheel_load_constants()

        # calculates wheel load formulas in pounds of force
        wheel_loads = calculations.calculate_wheel_loads(df_cleaned).copy()

        plots_wheel_load = make_plot(wheel_loads)
        return plots_wheel_load.plot_wheel_load_vs_time(wheel_loads)

    def damper_velocity_vs_time_client(self):
        velocity_df = calculations.calculate_velocities()
        plots = make_plot(velocity_df)
        fig = plots.plot_wheel_velocity_vs_time()
        #fig.show()
        return fig

    def damper_force_vs_time_client(self):
        dampening_force_df = calculations.estimate_damping_force()
        plots = make_plot(dampening_force_df)
        fig = plots.plot_damper_force_vs_time()
        #fig.show()
        return fig

    def linpot_vs_time_client(self):
        converted_data = conversions.convert_voltage_to_mm()
        plots = make_plot(converted_data)
        fig = plots.plot_linpot_vs_time()
        #fig.show()
        return fig

    def accel_vs_time_client(self):
        accel_g = conversions.convert_acel_to_g()
        print(accel_g)
        plots = make_plot(accel_g)
        fig = plots.plot_accel_vs_time()
        #fig.show()
        return fig

    def pitch_roll_client(self):
        x_y_z_low_pass_data = conversions.clean_acel_data()
        pitch_roll = conversions.generate_pitch_roll_df(x_y_z_low_pass_data)
        plots = make_plot(pitch_roll)
        fig = plots.plot_pitch_roll_vs_time()
        #fig.show()
        return fig


def main():
    client_instance = client()
    try:
        client_instance.damper_velocity_vs_time_client()
        client_instance.damper_force_vs_time_client()
        client_instance.wheel_load_client()
        client_instance.linpot_vs_time_client()
        client_instance.accel_vs_time_client()
        client_instance.pitch_roll_client()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
