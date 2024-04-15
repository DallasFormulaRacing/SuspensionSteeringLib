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

def main():
    client_instance = client()
    try:
        pass
        client_instance.wheel_load_handler()
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
