from deprecated.Visualizer import Visualizer
import plotly.express as px


class make_plot:

    def __init__(self, data):
        self.vis = Visualizer(data)
        self.data = data

    def plot_wheel_load_vs_time(self):
        fig = px.line(self.data, x="Time",
                      y=["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"],
                      title="Wheel Load Over Time")
        return fig

    def plot_wheel_load_vs_acceleration(self):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["X", "Y", "Z"]  # acceleration
        units = "lbf"
        self.vis.plot(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load", units)

        fig = px.scatter(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load", units)
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

    # TODO do we need this method ?
    def plot_damper_force_vs_displacement(self, Damper):
        y_columns = ["Damping Force Front Right", "Damping Force Front Left", "Damping Force Rear Right", "Damping Force Rear Left"]
        x_columns = ["Displacement Front Right", "Displacement Front Left", "Displacement Rear Right", "Displacement Rear Left"]
        units = "mm"
        vis = Visualizer(Damper.data)
        vis.plot_line(y_columns, x_columns, "Force Vs Displacement",  "Force", "Displacement", units)
