import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Visualizer:

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













    ## Below not in use
    def plot1(self, columns): 
        Force_FL = columns[0]
        Accel = columns[4]
        fig1 = px.scatter(self.wheel_load_df, x=Accel,
                         y=Force_FL)
        fig1.show()

    def plot_wheel_load_vs_time(self) -> None:
        fig1 = px.scatter(self.wheel_load_df, x="time",
                         y="F_LF")
        fig1.show()
        fig2 = px.scatter(self.wheel_load_df, x="time",
                         y="F_RF")
        fig2.show()
        fig3 = px.scatter(self.wheel_load_df, x="time",
                         y="F_RL")
        fig3.show()
        fig4 = px.scatter(self.wheel_load_df, x="time",
                         y="F_RR")
        fig4.show()

    def plot_wheel_load_vs_accel(self) -> None:
        fig1 = px.scatter(self.wheel_load_df, x="acceleration",
                         y="F_LF")
        fig1.show()
        fig2 = px.scatter(self.wheel_load_df, x="acceleration",
                         y="F_RF")
        fig2.show()
        fig3 = px.scatter(self.wheel_load_df, x="acceleration",
                         y="F_RL")
        fig3.show()
        fig4 = px.scatter(self.wheel_load_df, x="acceleration",
                         y="F_RR")
        fig4.show()