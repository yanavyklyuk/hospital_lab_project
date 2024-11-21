from bokeh.models import (ColumnDataSource, DataTable, TableColumn, HoverTool, FactorRange)
from bokeh.plotting import figure
import pandas as pd


def create_concurrency_graph():
    concurrency_dataframe = pd.DataFrame(
        {
            'processes': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5],
            'threads': [1, 2, 5, 10, 25, 50, 1, 2, 5, 10, 25, 50, 1, 2, 5, 10, 25, 50, 1, 2, 5, 10, 25, 50, 1, 2, 5, 10, 25, 50],
            'time': [12.48314905166626, 6.409812688827515, 6.107515573501587, 6.3299524784088135, 6.21195125579834,
                     6.563396692276001, 6.549526214599609, 6.656538724899292, 6.376149654388428, 6.9542014598846436,
                     6.562734127044678, 7.212470054626465, 6.680176496505737, 7.727933168411255, 7.36177396774292,
                     7.039641857147217, 8.451636791229248, 6.243313312530518, 7.572986364364624, 8.709786653518677,
                     7.539781332015991, 8.672459840774536, 7.397760629653931, 6.853748083114624, 9.435168504714966,
                     7.541523694992065, 8.919311046600342, 7.884115219116211, 8.50341010093689, 6.943810701370239]
        }
    )

    concurrency_dataframe['x'] = list(zip(concurrency_dataframe['processes'], concurrency_dataframe['threads']))

    # Підготовка даних для Bokeh
    x = [str(i) + '-' + str(j) for i, j in concurrency_dataframe[['processes', 'threads']].values]
    counts = concurrency_dataframe['time'].values

    # Створюємо джерело даних
    source = ColumnDataSource(data=dict(x=x, counts=counts, processes=concurrency_dataframe['processes'],
                                        threads=concurrency_dataframe['threads'], time=concurrency_dataframe['time']))

    # Створення графіка
    concurrency = figure(x_range=FactorRange(*x), height=350, title="Execution Time by Processes and Threads",
                         toolbar_location=None, tools="")

    # Малюємо стовпці
    concurrency.vbar(x='x', top='counts', width=0.9, source=source)

    # Додаємо інтерактивні підказки
    hover = HoverTool()
    hover.tooltips = [("Processes", "@processes"), ("Threads", "@threads"), ("Time", "@time")]
    concurrency.add_tools(hover)

    # Налаштування графіка
    concurrency.y_range.start = 0
    concurrency.x_range.range_padding = 0.1
    concurrency.xaxis.major_label_orientation = 1
    concurrency.xgrid.grid_line_color = None
    concurrency.xaxis.axis_label = "Processes - Threads"
    concurrency.yaxis.axis_label = "Execution Time (s)"

    concurrency.y_range.start = 0
    concurrency.x_range.range_padding = 0.1
    concurrency.xaxis.major_label_orientation = 1
    concurrency.xgrid.grid_line_color = None
    concurrency.xaxis.axis_label = "Processes - Threads"
    concurrency.yaxis.axis_label = "Execution Time (s)"

    stats_concurrency = concurrency_dataframe['time'].describe().reset_index()
    stats_concurrency.columns = ['Statistic', 'Value']

    # Створюємо джерело даних для таблиці статистики
    stats_source = ColumnDataSource(stats_concurrency)

    # Створюємо таблицю статистики
    columns = [
        TableColumn(field="Statistic", title="Statistic"),
        TableColumn(field="Value", title="Value")
    ]
    concurrency_table = DataTable(source=stats_source, columns=columns, width=400, height=280)

    return concurrency, concurrency_table
