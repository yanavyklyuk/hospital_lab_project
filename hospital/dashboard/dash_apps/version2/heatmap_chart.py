from bokeh.models import (ColumnDataSource, DataTable, TableColumn, HoverTool, ColorBar)
from bokeh.plotting import figure
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap

from heatmap_chart_data import get_experience_dataframe


def create_heatmap_chart():
    df_heatmap = get_experience_dataframe()
    source_heatmap = ColumnDataSource(df_heatmap)

    heatmap_chart = figure(
        title="Doctor Distribution by Experience and Appointments",
        x_range=df_heatmap['experience_category'].cat.categories.tolist(),
        y_range=df_heatmap['appointment_category'].cat.categories.tolist(),
        x_axis_location="above",
        height=600,
        width=800,
        tools="pan, wheel_zoom, box_zoom, reset",
        toolbar_location="right"
    )

    color_mapper = linear_cmap(
        field_name='doctor_count',
        palette=Viridis256,
        low=df_heatmap['doctor_count'].min(),
        high=df_heatmap['doctor_count'].max()
    )

    heatmap_chart.rect(
        x="experience_category",
        y="appointment_category",
        width=1,
        height=1,
        source=source_heatmap,
        line_color=None,
        fill_color=color_mapper
    )

    hover = HoverTool(
        tooltips=[
            ("Experience", "@experience_category"),
            ("Appointments", "@appointment_category"),
            ("Doctors", "@doctor_count")
        ]
    )
    heatmap_chart.add_tools(hover)

    color_bar = ColorBar(
        color_mapper=color_mapper['transform'],
        width=8,
        location=(0, 0),
        title="Number of Doctors"
    )
    heatmap_chart.add_layout(color_bar, 'right')

    stats_heatmap = df_heatmap['doctor_count'].describe().reset_index()
    stats_heatmap.columns = ['Statistic', 'Value']
    source_stats_heatmap = ColumnDataSource(stats_heatmap)

    columns_heatmap_stats = [
        TableColumn(field="Statistic", title="Statistic"),
        TableColumn(field="Value", title="Value")
    ]

    table_heatmap_stats = DataTable(
        source=source_stats_heatmap,
        columns=columns_heatmap_stats,
        height=300,
        width=400
    )

    return heatmap_chart, table_heatmap_stats
