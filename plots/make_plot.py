import plotly.express as px
import pandas as pd

class make_plot:
    def __init__(self, data): 
        self.data = data

    def plot_wheel_load_vs_time(self, data_wheel_load: pd.DataFrame):
        fig = px.scatter(data_wheel_load,
                            x="Time",
                            y=["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"])
        fig.update_layout(
            title="wheel load data",
            yaxis_title="Wheel Load (lbf)",
            xaxis_title="Time",
        )
        return fig
    
    def plot_linpot_vs_time(self):
        fig = px.line(self.data, x="Time", y=["Front Left", "Rear Left", "Rear Right", "Front Right"], title='Linpot vs Time')
        return fig

    def plot_accel_vs_time(self):
        fig = px.line(self.data, x="Time", y=["X", "Y", "Z"], title='Acceleration vs Time')
        return fig

    def plot_pitch_roll_vs_time(self):
        fig = px.line(self.data, x="Time", y=["Pitch", "Roll"], title='Pitch and Roll vs Time')
        return fig

    def plot_wheel_velocity_vs_time(self):
        fig = px.line(self.data, x="Time", y=["Velocity Front Right", "Velocity Front Left",
                      "Velocity Rear Right", "Velocity Rear Left"], title='Wheel Velocity vs Time')
        return fig

    def plot_damper_force_vs_velocity(self):

        fig = px.line(self.data, x="Time",
                      y=["Damping Force Front Right", "Damping Force Front Left", "Damping Force Rear Right", "Damping Force Rear Left"],
                      title='Damper Force vs Velocity')
        return fig
