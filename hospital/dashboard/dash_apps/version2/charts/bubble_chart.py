from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, DataTable, TableColumn
from bokeh.transform import linear_cmap
from bokeh.layouts import column
from bokeh.io import output_notebook
import pandas as pd


def create_bubble_chart(df):
    source = ColumnDataSource(df)
    mapper = LinearColorMapper(
        palette="Viridis256",
        low=df['time'].min(),
        high=df['time'].max()
    )

    p = figure(
        title="3D Concurrency Analysis: Processes vs Threads vs Time",
        x_axis_label="Number of Threads",
        y_axis_label="Number of Processes",
        tooltips=[
            ("Threads", "@threads"),
            ("Processes", "@processes"),
            ("Time", "@time"),
        ],
        width=800,
        height=600,
    )

    p.scatter(
        x='threads',
        y='processes',
        size='time',
        source=source,
        fill_color=linear_cmap('time', 'Viridis256', df['time'].min(), df['time'].max()),
        line_color=None,
        alpha=0.7
    )

    color_bar = ColorBar(
        color_mapper=mapper,
        label_standoff=12,
        location=(0, 0),
        title="Execution Time (s)"
    )
    p.add_layout(color_bar, 'right')

    return p


def describe_to_table(df):
    if df.empty:
        return None

    description = df.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    source = ColumnDataSource(description_reset)

    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]

    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table