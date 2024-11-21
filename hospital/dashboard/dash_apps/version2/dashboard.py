from bokeh.layouts import column, row
from bokeh.models import Select, Slider, ColumnDataSource, DataTable, TableColumn, HoverTool, PanTool, WheelZoomTool, BoxZoomTool, ResetTool
from bokeh.plotting import curdoc, figure
import numpy as np
from bokeh.palettes import Category20c

from pie_chart_data import get_appointments
from map_chart_data import get_disease_histories, get_diseases
from histogram_chart_data import get_disease_histories_h
from heatmap_chart_data import get_experience_dataframe
from linear_chart_data import get_disease_history_seasons_dataframe

# Data Preparation
df_pie = get_appointments()
#df_map = get_disease_histories()
#df_histogram = get_disease_histories_h()
##df_heatmap = get_experience_dataframe()
#df_linear = get_disease_history_seasons_dataframe()

# ColumnDataSource Initialization
#source_map = ColumnDataSource(df_map)
#source_hist = ColumnDataSource(df_histogram)
#source_heatmap = ColumnDataSource(df_heatmap)
#source_linear = ColumnDataSource(df_linear)

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

# Bar Chart (Map Simulation)
#map_chart = figure(title="Global Disease Cases", height=350, width=350)
#map_chart.vbar(x="patient_country", top="Cases", width=0.9, source=source_map)

# Linear Chart
#linear_chart = figure(title="Disease History Seasons", height=350, width=600)
#linear_chart.line("start_month", "disease_count", source=source_linear, line_width=2)

# Table for Pie Chart
stats_df.columns = ['Statistic', 'Value']
source_stats = ColumnDataSource(stats_df)
columns_pie = [
    TableColumn(field="Statistic", title="Metric"),
    TableColumn(field="Value", title="Value")
]
table_pie = DataTable(source=source_stats, columns=columns_pie, height=300, width=400)

# Table for Heatmap
#columns_heatmap = [TableColumn(field="doctor_name", title="Doctor"), TableColumn(field="doctor_count", title="Patients Treated")]
#table_heatmap = DataTable(source=source_heatmap, columns=columns_heatmap, height=300, width=350)

# Dropdowns and Sliders
"""disease_dropdown = Select(
    title="Select Disease",
    value="All",
    options=["All"] + [(disease['value'], disease['label']) for disease in get_diseases(df_map)]
)
year_slider = Slider(start=2015, end=2025, value=2020, step=1, title="Select Year")

# Callback Functions
def update_map(attr, old, new):
    selected_disease = disease_dropdown.value
    if selected_disease == "All":
        filtered_data = df_map
    else:
        filtered_data = df_map[df_map["patient_country"] == selected_disease]
    source_map.data = ColumnDataSource.from_df(filtered_data)

disease_dropdown.on_change("value", update_map)"""

# Layout
layout = column(
    row(pie_chart, table_pie),
    #row(disease_dropdown, map_chart),
    #row(linear_chart, table_heatmap),
    #year_slider
)

# Add to Document
curdoc().add_root(layout)
curdoc().title = "Bokeh Dashboard"
