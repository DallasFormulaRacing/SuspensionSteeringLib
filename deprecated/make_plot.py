import deprecated.Visualizer as Visualizer
from deprecated.Visualizer import Visualizer


class make_plot:
    def plot_wheel_load_vs_time(WL):
        Forces = [WL.data["Force Front Left (lbs)"], WL.data["Force Front Right (lbs)"],
                  WL.data["Force Rear Left (lbs)"], WL.data["Force Rear Right (lbs)"]]
        columns = [Forces[0], Forces[1], Forces[2], Forces[3], WL.data["Time"]]
        vis = Visualizer(WL.data)
        vis.plot(columns, "Time")

    def plot_wheel_load_vs_acceleration(WL):
        Forces = [WL.data["Force Front Left (lbs)"], WL.data["Force Front Right (lbs)"],
                  WL.data["Force Rear Left (lbs)"], WL.data["Force Rear Right (lbs)"]]
        columns = [Forces[0], Forces[1], Forces[2], Forces[3], WL.data["Acceleration"]]
        vis = Visualizer(WL.data)
        vis.plot(columns, "Acceleration")
  def plot_wheel_load_vs_acceleration2(self, accel_df: pd.DataFrame, wheel_load: pd.DataFrame):
        fig = px.line(wheel_load,
                        y=["Force Front Left", "Force Front Right", "Force Rear Left", "Force Rear Right"],
                        x=accel_df["X"])
        fig.update_layout(
            title="Wheel Load vs Acceleration data",
            xaxis_title="Acceleration (g)",
            yaxis_title="Wheel Load (lbf)",
        )
        #fig.show()
        return fig