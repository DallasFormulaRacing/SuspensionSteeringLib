import plotly.express as px
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame = None):
        self.df = data
        self.df2 = data2

    ''''''
    # Customizable plot function for any title, units, axis titles
    # Accepts any number of variables in the y axis and x axis
    # y_columns is the quantities we care about plotting or the dependent variable
    # x_columns is the quantities that is in the "versus" part or the independent variable
    # title is how you want to label the whole graph 
    # x_axis title is the label of the x axis and needs to be a string
    # y_axis title is the label of the y axis and needs to be a string
    # units is the units of the y axis (lbf, g, mm/s, etc.)
    # plot_type is the type of plot you want, and the values currently accepted are:
    # scatter and line
    ''''''
    def plot(self, y_columns: list, x_columns: list, title: str, x_axis_title: str, y_axis_title: str, units: str, plot_type: str):
        plot_num = 0
        match plot_type:
            case "scatter":
                plot_num = 0

            case "line":
                plot_num = 1

            case _:
                plot_num = 0

        for i in range(0, len(x_columns)):
            if plot_num == 0:
                fig = px.scatter(self.df,
                                 x=x_columns[i],
                                 y=y_columns)
            elif plot_num == 1:
                fig = px.line(self.df,
                              x=x_columns[i],
                              y=y_columns)
            fig.update_layout(
                title=f"{title} data",
                yaxis_title=f"{y_axis_title} ({units})",
                xaxis_title=f"{x_axis_title}",
            )
            fig.show()
            return fig

    def plot_new(self, y_columns: list, x_columns: list, title: str, x_axis_title: str, y_axis_title: str, units: str, plot_type: str):
        plot_num = 0
        match plot_type:
            case "scatter":
                plot_num = 0

            case "line":
                plot_num = 1

            case _:
                plot_num = 0

        for i in range(0, len(x_columns)):
            if plot_num == 0:
                fig = px.scatter(self.df,
                                 x=x_columns[i],
                                 y=y_columns)
            elif plot_num == 1:
                fig = px.line(
                              x=self.df2[x_columns],
                              y=self.df[y_columns])
            fig.update_layout(
                title=f"{title} data",
                yaxis_title=f"{y_axis_title} ({units})",
                xaxis_title=f"{x_axis_title}",
            )
            fig.show()
            return fig
