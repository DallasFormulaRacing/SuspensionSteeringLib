import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame):
        self.wheel_load_df = data

    def plot(self, columns): 
        F_FL = columns[0]
        Accel = columns[4]
        fig1 = px.scatter(self.wheel_load_df, x=F_FL,
                         y=Accel)
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