from conversions.conversions import Conversions
from calculations.calculations import Calculations
from plots.make_plot import make_plot
import traceback
import pandas as pd

conversions = Conversions("data\\output2_linpot_2023-10-14_13-23-28.csv", "data\\output2_analog_2023-10-14_13-18-15.csv")
calculations = Calculations("data\\output2_linpot_2023-10-14_13-23-28.csv")
#conversions.clean_data(conversions.data)


class handler:

    def wheel_load_handler(self):
        # loads and prepares initial data
        data_linpot = conversions.data_linpot
        data_accel = conversions.data_accel
        data_linpot_converted = conversions.convert_voltage_to_in(data_linpot)
        data_accel_converted = conversions.convert_xl_g(data_accel)
        df_cleaned = conversions.clean_data(data_linpot_converted)
        calculations.data = df_cleaned
        calculations.data2 = conversions.data_accel
        calculations.calculate_wheel_load_constants()
        
        # calculates wheel load formulas in pounds of force
        wheel_loads = calculations.calculate_wheel_loads(df_cleaned)

        conversions.convert_time(wheel_loads)
        conversions.convert_time(data_accel_converted)
        plots_wheel_load = make_plot(wheel_loads)
        plots_accel = make_plot(data_accel_converted)
        plots_wheel_load.plot_wheel_load_vs_time(wheel_loads)
        plots_accel.plot_acceleration_vs_time(data_accel_converted)
        return plots_wheel_load.plot_wheel_load_vs_acceleration(data_accel_converted, wheel_loads)

    def wheel_damper_handler(self):
        # call the convert to mm method from conversions
        displacement_df = calculations.calculate_displacement()
        time_constant = calculations.calculate_time_constant()
        velocity_df = calculations.calculate_velocities(displacement_df, time_constant)


def main():
    handler_instance = handler()
    try:
        handler_instance.wheel_load_handler()
        handler_instance.wheel_damper_handler()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
