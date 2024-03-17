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
        # todo: return dataframe
        df = conversions.data
        df_xl = conversions.data2
        df_converted = conversions.convert_voltage_to_in(df)
        conversions.convert_xl_g()
        df_cleaned = conversions.clean_data(df_converted)
        calculations.data = df_cleaned
        calculations.data2 = conversions.data2
        df_xl_goal = calculations.data2

        # calculating constants
        calculations.calculate_wheel_load_constants()
        
        # calculates wheel load formulas in pounds of force
        wheel_loads = calculations.calculate_wheel_loads(df_converted)

        conversions.convert_time(wheel_loads)
        conversions.convert_time(df_xl_goal)
        plots = make_plot(wheel_loads)
        plots3 = make_plot(df_xl_goal)
        plots.plot_wheel_load_vs_time()
        return plots3.plot_wheel_load_vs_acceleration(wheel_loads)

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
