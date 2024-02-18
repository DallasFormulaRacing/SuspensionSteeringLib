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
        vis = Visualizer(Damper.data)
        vis.plot_line(y_columns, x_columns, "Velocity Vs Time",  "Velocity", "Time", units)

    def plot_damper_force_vs_velocity(self, Damper):
        y_columns = ["Damping Force Front Right", "Damping Force Front Left", "Damping Force Rear Right", "Damping Force Rear Left"]
        x_columns = ["Velocity Front Right", "Velocity Front Left", "Velocity Rear Right", "Velocity Rear Left"]
        units = "mm/s"
        vis = Visualizer(Damper.data)
        vis.plot_line(y_columns, x_columns, "Force Vs Velocity",  "Force", "Velocity", units)
    
    def plot_damper_force_vs_displacement(self, Damper):
        y_columns = ["Damping Force Front Right", "Damping Force Front Left", "Damping Force Rear Right", "Damping Force Rear Left"]
        x_columns = ["Displacement Front Right", "Displacement Front Left", "Displacement Rear Right", "Displacement Rear Left"]
        units = "mm"
        vis = Visualizer(Damper.data)
        vis.plot_line(y_columns, x_columns, "Force Vs Displacement",  "Force", "Displacement", units)
