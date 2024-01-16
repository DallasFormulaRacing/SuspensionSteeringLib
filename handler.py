from conversions import conversions
from calculations import calculations
from plots import make_plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class handler:
    calculations = calculations.calculations("data\output2_linpot_2023-10-14_13-23-28.csv")
    conversions = conversions.conversions("data\output2_linpot_2023-10-14_13-23-28.csv")
    conversions.convert_voltage_to_in()
    conversions.convert_time(conversions.data)
    conversions.clean_data()
    calculations.data = conversions.data
    calculations.wheel_ratio_front = conversions.calculate_wheeel_ratio_front()
    calculations.wheel_ratio_rear = conversions.calculate_wheel_ratio_rear()
    calculations.wheel_ratio_roll_front = conversions.calculate_wheel_ratio_roll_front()
    calculations.wheel_ratio_roll_rear = conversions.calculate_wheel_ratio_roll_rear()
    calculations.K_H = conversions.calculate_K_H_K_P()
    calculations.K_P = calculations.K_H
    calculations.K_R = conversions.calculate_K_R_K_W()
    calculations.K_W = calculations.K_R
    calculations.wheel_load_const_a = conversions.calculate_a_b()
    calculations.wheel_load_const_b = calculations.wheel_load_const_a
    calculations.q = conversions.calculate_q_w()
    calculations.w = calculations.q
    calculations.calculate_force_front_left()
    calculations.calculate_force_front_right()
    calculations.calculate_force_rear_left()
    calculations.calculate_force_rear_right()
    make_plot.make_plot.plot_wheel_load_vs_time(calculations)   


    def __init__(self, data: pd.DataFrame):
        self.df = data

    def plot(self, y_columns, x_columns, title, x_axis_title, y_axis_title): 
        y_column_names = []
        for i in range(0, len(y_columns)):
            y_column_names.append(y_columns[i].name)
        
        x_column_names = []
        for j in range(0, len(x_columns)):
            x_column_names.append(x_columns[j].name)
        for k in range(0, len(x_column_names)):
            fig = px.scatter(self.df,
                            x = x_column_names[k],
                            y = y_column_names,
                            color_discrete_sequence = px.colors.qualitative.Vivid)
            fig.update_layout(
                title= f"{title}",
                yaxis_title= f"{y_axis_title}",
                xaxis_title= f"{x_axis_title}",
            )
            fig.show()
