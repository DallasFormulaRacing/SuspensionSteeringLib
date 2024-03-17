from visualizer import Visualizer


class make_plot:
    def __init__(self, data):
        self.vis = Visualizer(data) 
        self.df = data

    def plot_wheel_load_vs_time(self):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["Time"]
        units = "lbf"
        return self.vis.plot(y_columns, x_columns, "Wheel Load", "Time", "Wheel Load", units, "scatter")

    def plot_wheel_load_vs_acceleration(self, data2):
        y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
        x_columns = ["X"]
        units = "lbf"
        self.vis2 = Visualizer(self.df, data2)
        return self.vis2.plot_new(x_columns[0], y_columns[0], "Wheel Load", "Acceleration", "Wheel Load", units, "line")

    def plot_acceleration_vs_time(self):
        y_columns = ["X", "Y", "Z"]
        x_columns = ["Time"]
        units = "g"
        return self.vis.plot(y_columns, x_columns, "Acceleration", "Time", "Acceleration", units, "line")