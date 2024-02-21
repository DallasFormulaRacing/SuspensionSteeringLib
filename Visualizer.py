import plotly.express as px
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame):
        self.df = data

    def plot(self, y_columns, x_columns, title, x_axis_title, y_axis_title, units):
        for i in range(0, len(x_columns)):
            fig = px.scatter(self.df,
                             x=x_columns[i],
                             y=y_columns,
                             color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(
                title=f"{title} data",
                yaxis_title=f"{y_axis_title} ({units})",
                xaxis_title=f"{x_axis_title}",
            )
            fig.show()

    def plot_line(self, y_columns, x_columns, title, x_axis_title, y_axis_title, units):
        for i in range(0, len(x_columns)):
            fig = px.line(self.df,
                          x=x_columns[i],
                          y=y_columns,
                          color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(
                title=f"{title} data",
                yaxis_title=f"{y_axis_title} ({units})",
                xaxis_title=f"{x_axis_title}",
            )
            fig.show()
