
import Visualizer
import WheelLoadHandler
class make_plot:
     def plot_wheel_load_vs_time():
            WL = WheelLoadHandler(0, 0, 0, 0,"output2_linpot_2023-10-14_13-23-28.csv")
            WL.calculate_consts()
            Forces = WL.calculate_force_equations()
            
            #columns = columns[WL.Force_LF, WL.Force_RL, WL.Force_RR, WL.Force_LR, WL.acceleration]
            columns = columns[Forces[0], Forces[1], Forces[2], Forces[3], WL.df["time"]]
            Visualizer.Visualizer.plot(columns)
            #return ""

     def plot_wheel_load_vs_acceleration():
            WL = WheelLoadHandler(0, 0, 0, 0,"output2_linpot_2023-10-14_13-23-28.csv")
            WL.calculate_consts()
            Forces = WL.calculate_force_equations()

            #columns = columns[WL.Force_LF, WL.Force_RL, WL.Force_RR, WL.Force_LR, WL.acceleration]
            columns = columns[Forces[0], Forces[1], Forces[2], Forces[3], WL.acceleration]
            Visualizer.Visualizer.plot(columns)
            #return ""