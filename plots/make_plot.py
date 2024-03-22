from visualizer import Visualizer
import plotly.express as px
import pandas as pd

class make_plot:
    def __init__(self, data):
        #self.vis = Visualizer(data) 
        self.df = data

    def plot_wheel_load_vs_time(self, data_wheel_load: pd.DataFrame):
        fig = px.scatter(data_wheel_load,
                            x="Time",
                            y=["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"])
        fig.update_layout(
            title="wheel load data",
            yaxis_title="Wheel Load (lbf)",
            xaxis_title="Time",
        )
        
        fig.show()
        return fig

    def plot_wheel_load_vs_acceleration(self, accel_df: pd.DataFrame, wheel_load: pd.DataFrame):
        fig = px.line(wheel_load,
                        y=["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"],
                        x=accel_df["X"])
        fig.update_layout(
            title="Wheel Load vs Acceleration data",
            xaxis_title="Acceleration (g)",
            yaxis_title="Wheel Load (lbf)",
        )
        fig.show()
        return fig

    def plot_acceleration_vs_time(self, accel_df):
        fig = px.line(accel_df,
                            x="Time",
                            y=["X", "Y", "Z"])
        fig.update_layout(
            title="Acceleromator data",
            yaxis_title="Acceleration (g)",
            xaxis_title="Time",
        )
        
        fig.show()
        return fig