from bokeh.models import (ColumnDataSource, HoverTool, PanTool, WheelZoomTool, BoxZoomTool, ResetTool,
                          DataTable, TableColumn)
from bokeh.plotting import figure
import numpy as np
from bokeh.palettes import Category20c

from pie_chart_data import get_appointments


def create_pie_chart():
    df_pie = get_appointments()
    stats_df = df_pie['favor_cost'].describe().reset_index()
    df_pie = df_pie.groupby('favor_name')['favor_cost'].sum().reset_index()
    df_pie['angle'] = df_pie["favor_cost"] / df_pie["favor_cost"].sum() * 2 * np.pi
    df_pie['percent'] = (df_pie["favor_cost"] / df_pie["favor_cost"].sum() * 100).round(2)
    df_pie['color'] = Category20c[len(df_pie)]
    df_pie['start_angle'] = np.concatenate([[0], np.cumsum(df_pie['angle'])[:-1]])
    df_pie['end_angle'] = np.cumsum(df_pie['angle'])

    source_pie = ColumnDataSource(df_pie)

    pie_chart = figure(title="Hospital Income", height=600, width=600, toolbar_location="right", tools="",
                       x_range=(-0.6, 1),
                       y_range=(0.7, 1.3),)
    pie_chart.add_tools(PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool())
    pie_chart.toolbar.active_scroll = WheelZoomTool()
    pie_chart.wedge(
        x=0, y=1, radius=0.4,
        start_angle= 'start_angle',
        end_angle='end_angle',
        fill_color="color",
        legend_field="favor_name",
        source=source_pie,
    )

    pie_chart.text(
        x=0.6 * np.cos((df_pie['start_angle'] + df_pie['end_angle']) / 2),
        y=1.6 * np.sin((df_pie['start_angle'] + df_pie['end_angle']) / 2),
        text_align="center",
        text_baseline="middle"
    )

    hover = HoverTool(
        tooltips=[
            ("Favor", "@favor_name"),
            ("Income", "@favor_cost"),
            ("Percent", "@percent%")
        ]
    )
    pie_chart.add_tools(hover)

    pie_chart.legend.title = "Services"
    pie_chart.legend.location = "top_right"

    stats_df.columns = ['Statistic', 'Value']
    source_stats = ColumnDataSource(stats_df)
    columns_pie = [
        TableColumn(field="Statistic", title="Metric"),
        TableColumn(field="Value", title="Value")
    ]
    table_pie = DataTable(source=source_stats, columns=columns_pie, height=300, width=400)

    return pie_chart, table_pie
