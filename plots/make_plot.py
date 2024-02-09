from Visualizer import Visualizer


class make_plot:
    def plot_wheel_load_vs_time(self, WL):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["Time"]
        units = "lbf"
        vis = Visualizer(WL.data)
        vis.plot(y_columns, x_columns, "Wheel Load", "Time", "Wheel Load", units)

    def plot_wheel_load_vs_acceleration(self, WL):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["X Axis, Y_Axis, Z_Axis"]  # acceleration
        units = "lbf"
        vis = Visualizer(WL.data)
        vis.plot(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load", units)

    def plot_damper_velocity_vs_time(self, Damper):
        y_columns = ["Velocity Front Right", "Velocity Front Left", "Velocity Rear Right", "Velocity Rear Left"]
        x_columns = ["Time"]
        units = "mm/s"
        vis = Visualizer(Damper.velocities_df)
        vis.plot_line(y_columns, x_columns, "Velocity Vs Time",  "Velocity", "Time", units)