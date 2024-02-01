from visualizer import Visualizer
import traceback


class make_plot:
    def __init__(self, data):
        self.vis = Visualizer(data) 

    def plot_wheel_load_vs_time(self):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["Time"]
        units = "lbf"
        try:
            self.vis.plot(y_columns, x_columns, "Wheel Load", "Time", "Wheel Load", units)
        except Exception:
            traceback.print_exc()

    def plot_wheel_load_vs_acceleration(self):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["X", "Y", "Z"]  # acceleration
        units = "lbf"
        try:
            self.vis.plot(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load", units)
        except Exception:
            traceback.print_exc()
