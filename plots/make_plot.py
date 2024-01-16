import Visualizer
from Visualizer import Visualizer

class make_plot:
     def plot_wheel_load_vs_time(WL):
            Forces = [WL.data["Force Front Left (lbs)"], WL.data["Force Front Right (lbs)"], WL.data["Force Rear Left (lbs)"], WL.data["Force Rear Right (lbs)"]]
            y_columns = [Forces[0], Forces[1], Forces[2], Forces[3]]
            x_columns = [WL.data["Time"]]
            vis = Visualizer(WL.data)
            vis.plot(y_columns, x_columns, "Wheel Load", "Time", "Wheel Load Data (lbs)")

     def plot_wheel_load_vs_acceleration(WL):
            Forces = [WL.data["Force Front Left (lbs)"], WL.data["Force Front Right (lbs)"], WL.data["Force Rear Left (lbs)"], WL.data["Force Rear Right (lbs)"]]
            y_columns = [Forces[0], Forces[1], Forces[2], Forces[3]]
            x_columns = [WL.data["Acceleration"]]
            vis = Visualizer(WL.data)
            vis.plot(y_columns, x_columns, "Wheel Load", "Acceleration", "Wheel Load Data (lbs)")