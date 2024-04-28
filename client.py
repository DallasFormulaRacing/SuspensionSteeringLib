from .conversions.conversions import Conversions
from .calculations.calculations import Calculations
from .plots.make_plot import make_plot
import traceback
import pandas as pd


class client:
    def __init__(self, df):
        #self.conversions.clean_data(self.conversions.data)
        self.conversions = Conversions(df)
        self.calculations = Calculations(df)

    def wheel_load_client(self):
        # loads and prepares initial data
        data_linpot = self.conversions.data.copy()
        linpot_switched = self.conversions.switch_columns(data_linpot)
        data_linpot_converted = self.conversions.convert_voltage_to_in(linpot_switched)
        df_linpot_cleaned = self.conversions.clean_linpot_data(data_linpot_converted)
        self.calculations.data = df_linpot_cleaned
        self.calculations.calculate_wheel_load_constants()

        # calculates wheel load formulas in pounds of force
        wheel_loads = self.calculations.calculate_wheel_loads(df_linpot_cleaned).copy()

        plots_wheel_load = make_plot(wheel_loads)
        return plots_wheel_load.plot_wheel_load_vs_time(wheel_loads)

    def damper_velocity_vs_time_client(self):
        #conversions.data = conversions.convert_time(conversions.data).copy()
        self.calculations.linpot_dataframe = self.conversions.switch_columns(self.conversions.data)   
        velocity_df = self.calculations.calculate_velocities()
        plots = make_plot(velocity_df)
        fig = plots.plot_wheel_velocity_vs_time()
        #fig.show()
        return fig

    def damper_force_vs_time_client(self):
        #conversions.data = conversions.convert_time(conversions.data).copy()   
        self.calculations.linpot_dataframe = self.conversions.switch_columns(self.conversions.data)  
        dampening_force_df = self.calculations.estimate_damping_force()
        plots = make_plot(dampening_force_df)
        fig = plots.plot_damper_force_vs_time()
        #fig.show()
        return fig

    def linpot_vs_time_client(self):
        data_linpot = self.conversions.data.copy()
        self.conversions.data = self.conversions.switch_columns(data_linpot)
        converted_data = self.conversions.convert_voltage_to_mm()
        plots = make_plot(converted_data)
        fig = plots.plot_linpot_vs_time()
        #fig.show()
        return fig

    def accel_vs_time_client(self):
        self.conversions.data = self.conversions.convert_time(self.conversions.data).copy()
        accel_g = self.conversions.convert_acel_to_g()
        #print(accel_g)
        plots = make_plot(accel_g)
        fig = plots.plot_accel_vs_time()
        #fig.show()
        return fig

    def pitch_roll_client(self):
        self.conversions.data = self.conversions.convert_time(self.conversions.data).copy()
        x_y_z_low_pass_data = self.conversions.clean_acel_data()
        pitch_roll = self.conversions.generate_pitch_roll_df(x_y_z_low_pass_data)
        plots = make_plot(pitch_roll)
        fig = plots.plot_pitch_roll_vs_time()
        #fig.show()
        return fig


#def main():
    #client_instance = client()
    #try:
        #client_instance.damper_velocity_vs_time_client()
        #client_instance.damper_force_vs_time_client()
        #client_instance.wheel_load_client()
        #client_instance.linpot_vs_time_client()
        #client_instance.accel_vs_time_client()
        #client_instance.pitch_roll_client()
    #except Exception:
        #traceback.print_exc()


#if __name__ == '__main__':
#    main()