from visualizer import Visualizer

class make_plot:
     def plot_wheel_load_vs_time(self, WL):
            y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
            x_columns = ["Time"]
            units = "lbf"
            vis = Visualizer(WL.data)
            vis.plot(y_columns, x_columns, "Wheel Load", "Time", "Wheel Load", units)

     def plot_wheel_load_vs_acceleration(self, WL):
            y_columns = ["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"]
            x_columns = ["X Axis, Y_Axis, Z_Axis"] # acceleration
            units = "lbf"
            vis = Visualizer(WL.data)
            vis.plot(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load", units)
            
     def plot_acceleration_vs_time(self, ACC):
            y_columns = ["X Axis, Y_Axis, Z_Axis"] # acceleration 
            x_columns = ["Time"]
            units = "m/s"
            vis = Visualizer(ACC.data)
            vis.plot(y_columns, x_columns, "Acceleration", "Time", "Acceleration", units)
