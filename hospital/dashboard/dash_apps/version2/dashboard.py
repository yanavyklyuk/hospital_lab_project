from bokeh.layouts import column, row
from bokeh.models import Select, Slider, ColumnDataSource, DataTable, TableColumn
from bokeh.plotting import curdoc, figure
from bokeh.io import show
import pandas as pd
import numpy as np

from ..data.pie_chart_data import get_appointments
from ..data.map_chart_data import get_disease_histories, get_diseases
from ..data.histogram_chart_data import get_disease_histories_h, get_diseases_h
from ..data.heatmap_chart_data import get_experience_dataframe
from ..data.linear_chart_data import get_disease_history_seasons_dataframe, get_diseases_l, get_years_l

# Data Preparation
df_pie = get_appointments()
df_map = get_disease_histories()
df_histogram = get_disease_histories_h()
df_heatmap = get_experience_dataframe()
df_linear = get_disease_history_seasons_dataframe()

# ColumnDataSource Initialization
source_pie = ColumnDataSource(df_pie)
source_map = ColumnDataSource(df_map)
source_hist = ColumnDataSource(df_histogram)
source_heatmap = ColumnDataSource(df_heatmap)
source_linear = ColumnDataSource(df_linear)

# Pie Chart
pie_chart = figure(title="Hospital Income", height=350, width=350, toolbar_location=None)
pie_chart.wedge(
    x=0, y=1, radius=0.4,
    start_angle=np.cumsum(df_pie["favor_cost"]) / df_pie["favor_cost"].sum() * 2 * np.pi,
    end_angle=np.cumsum(df_pie["favor_cost"]) / df_pie["favor_cost"].sum() * 2 * np.pi,
    fill_color="blue",
    legend_field="favor_name",
    source=source_pie
)

# Bar Chart (Map Simulation)
map_chart = figure(title="Global Disease Cases", height=350, width=350)
map_chart.vbar(x="patient_country", top="Cases", width=0.9, source=source_map)

# Linear Chart
linear_chart = figure(title="Disease History Seasons", height=350, width=600)
linear_chart.line("start_month", "disease_count", source=source_linear, line_width=2)

# Table for Pie Chart
columns_pie = [TableColumn(field="favor_name", title="Favor"), TableColumn(field="favor_cost", title="Total Income")]
table_pie = DataTable(source=source_pie, columns=columns_pie, height=300, width=350)

# Table for Heatmap
columns_heatmap = [TableColumn(field="doctor_name", title="Doctor"), TableColumn(field="doctor_count", title="Patients Treated")]
table_heatmap = DataTable(source=source_heatmap, columns=columns_heatmap, height=300, width=350)

# Dropdowns and Sliders
disease_dropdown = Select(title="Select Disease", value="All", options=["All"] + get_diseases(df_map))
year_slider = Slider(start=2015, end=2025, value=2020, step=1, title="Select Year")

# Callback Functions
def update_map(attr, old, new):
    selected_disease = disease_dropdown.value
    if selected_disease == "All":
        filtered_data = df_map
    else:
        filtered_data = df_map[df_map["patient_country"] == selected_disease]
    source_map.data = ColumnDataSource.from_df(filtered_data)

disease_dropdown.on_change("value", update_map)

# Layout
layout = column(
    row(pie_chart, table_pie),
    row(disease_dropdown, map_chart),
    row(linear_chart, table_heatmap),
    year_slider
)

# Add to Document
curdoc().add_root(layout)
curdoc().title = "Bokeh Dashboard"
