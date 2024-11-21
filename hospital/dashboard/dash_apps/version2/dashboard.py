from datetime import datetime

from bokeh.layouts import column, row
from bokeh.models import (Select, Slider, ColumnDataSource, DataTable, TableColumn, HoverTool, PanTool, WheelZoomTool, BoxZoomTool,
                          ResetTool, GeoJSONDataSource, ColorBar, FactorRange)
from bokeh.plotting import curdoc, figure
import numpy as np
import pandas as pd
import json
import requests
from bokeh.palettes import Category20c, Viridis256
from bokeh.transform import linear_cmap, dodge

from pie_chart_data import get_appointments
from map_chart_data import get_disease_histories, get_diseases
from histogram_chart_data import get_disease_histories_h
from heatmap_chart_data import get_experience_dataframe
from linear_chart_data import get_disease_history_seasons_dataframe
from concurrency_data import get_concurrency_dataframe

df_pie = get_appointments()
df_map = get_disease_histories()

def convert_geojson_types(data):
    if isinstance(data, dict):
        return {key: convert_geojson_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_geojson_types(item) for item in data]
    elif isinstance(data, pd._libs.missing.NAType):  # Якщо є NAType з Pandas
        return None
    elif isinstance(data, (np.int64, np.float64)):  # Конвертація числових типів Pandas
        return int(data) if isinstance(data, np.int64) else float(data)
    return data

def preprocess_data(df):
    if 'patient_country' not in df.columns:
        raise ValueError("DataFrame does not contain the required column 'patient_country'.")
    country_counts = df['patient_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Cases']
    return country_counts

url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
response = requests.get(url)
if response.status_code == 200:
    geojson_data = response.json()
else:
    raise ValueError(f"Failed to fetch GeoJSON: {response.status_code}")

# GeoJSONDataSource
geo_source = GeoJSONDataSource(geojson=json.dumps(geojson_data))


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

country_counts = preprocess_data(df_map)
country_counts['color'] = country_counts['Cases'].apply(lambda x: 0 if x == 0 else x)
for feature in geojson_data['features']:
    country_name = feature['properties']['ADMIN']
    if country_name in country_counts['Country'].values:
        # Знайдено відповідну країну, додаємо кількість випадків
        cases = country_counts.loc[country_counts['Country'] == country_name, 'Cases'].values[0]
        feature['properties']['Cases'] = cases
    else:
        # Якщо країну не знайдено, встановлюємо Cases = 0
        feature['properties']['Cases'] = 0

geojson_data = convert_geojson_types(geojson_data)

# GeoJSONDataSource
geo_source = GeoJSONDataSource(geojson=json.dumps(geojson_data))
country_counts['color'] = country_counts['Cases'].apply(lambda x: 0 if x == 0 else x)
color_mapper = linear_cmap(
    field_name="Cases", palette=Viridis256, low=1, high=country_counts['Cases'].max()
)

map_chart = figure(
    title="Global Disease Cases",
    height=600,
    width=900,
    toolbar_location="right",
    tools="pan, wheel_zoom, box_zoom, reset"
)

map_chart.patches(
    'xs', 'ys', source=geo_source,
    fill_color=color_mapper, line_color="white", line_width=0.5
)

map_chart.x_range.start = -25
map_chart.x_range.end = 45
map_chart.y_range.start = 35
map_chart.y_range.end = 75

color_bar = ColorBar(color_mapper=color_mapper['transform'], width=8, location=(0, 0))
map_chart.add_layout(color_bar, 'right')

# Додавання HoverTool
hover_tool = HoverTool(tooltips=[
    ("Country", "@ADMIN"),
    ("Cases", "@Cases")
])
map_chart.add_tools(hover_tool)

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

stats_map = country_counts['Cases'].describe().reset_index()
stats_map.columns = ['Statistic', 'Value']
columns_stats = [
    TableColumn(field="Statistic", title="Statistic"),
    TableColumn(field="Value", title="Value")
]
source_stats_map = ColumnDataSource(stats_map)

table_map = DataTable(source=source_stats_map, columns=columns_stats, height=300, width=400)
# Table for Heatmap
#columns_heatmap = [TableColumn(field="doctor_name", title="Doctor"), TableColumn(field="doctor_count", title="Patients Treated")]
#table_heatmap = DataTable(source=source_heatmap, columns=columns_heatmap, height=300, width=350)

# Dropdowns and Sliders
disease_dropdown = Select(
    title="Select Disease",
    value="All",
    options=["All"] + [(disease['value'], disease['label']) for disease in get_diseases(df_map)]
)

# Callback Functions
def update_map(attr, old, new):
    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    response = requests.get(url)
    if response.status_code == 200:
        geojson_data = response.json()  # This is where geojson_data gets its value
    else:
        # Handle the case where the request fails
        raise ValueError(f"Failed to fetch GeoJSON: {response.status_code}")
    selected_disease = disease_dropdown.value
    if selected_disease == "All":
        filtered_data = df_map
    else:
        filtered_data = df_map[df_map["disease"] == selected_disease]

    # Reprocess data for the map chart
    country_counts = preprocess_data(filtered_data)

    country_counts['color'] = country_counts['Cases'].apply(lambda x: 0 if x == 0 else x)

    # Update geo_source for the map chart
    for feature in geojson_data['features']:
        country_name = feature['properties']['ADMIN']
        if country_name in country_counts['Country'].values:
            cases = country_counts.loc[country_counts['Country'] == country_name, 'Cases'].values[0]
            feature['properties']['Cases'] = cases
        else:
            feature['properties']['Cases'] = 0

    geojson_data = convert_geojson_types(geojson_data)

    # Оновлюємо GeoJSONDataSource
    geo_source.geojson = json.dumps(geojson_data)

    # Оновлюємо color_mapper для нових значень
    min_cases = country_counts['Cases'].min()  # Мінімум
    max_cases = country_counts['Cases'].max()  # Максимум

    # Якщо мінімум дорівнює 0, ми налаштовуємо його так, щоб 0 було відображене білим
    color_mapper = linear_cmap(
        field_name="Cases",
        palette=Viridis256,
        low=min_cases if min_cases > 0 else 1,  # мінімум 1, якщо є 0
        high=max_cases
    )

    # Оновлюємо колірну шкалу
    color_bar.color_mapper = color_mapper['transform']

    # Оновлюємо кольори на карті
    map_chart.patches(
        'xs', 'ys', source=geo_source,
        fill_color=color_mapper, line_color="white", line_width=0.5
    )

    stats_map = country_counts['Cases'].describe().reset_index()
    stats_map.columns = ['Statistic', 'Value']
    source_stats_map.data = stats_map.to_dict(orient='list')


disease_dropdown.on_change("value", update_map)

df_histogram = get_disease_histories_h()


def prepare_histogram_data(disease):
    if disease == "All":
        filtered_data = df_histogram
    else:
        filtered_data = df_histogram[df_histogram['disease'] == disease]

    grouped = filtered_data.groupby('patient_age')['duration'].mean().reset_index()
    grouped.columns = ['patient_age', 'avg_duration']
    return grouped



histogram_data = prepare_histogram_data("All")
source_histogram = ColumnDataSource(histogram_data)

histogram_chart = figure(
    title="Average Disease Duration by Age",
    x_axis_label="Patient Age",
    y_axis_label="Average Duration",
    height=350,
    width=600,
    toolbar_location="right",
    tools="pan, wheel_zoom, box_zoom, reset"
)

histogram_chart.vbar(
    x='patient_age',
    top='avg_duration',
    width=0.8,
    source=source_histogram,
    color="blue",
    fill_alpha=0.7,
    line_alpha=0.8
)

hover_hist = HoverTool(
    tooltips=[("Age", "@patient_age"), ("Avg Duration", "@avg_duration")]
)
histogram_chart.add_tools(hover_hist)

histogram_disease_dropdown = Select(
    title="Select Disease for Histogram",
    value="All",
    options=["All"] + list(df_histogram['disease'].unique())
)


def prepare_histogram_statistics(disease):
    if disease == "All":
        filtered_data = df_histogram
    else:
        filtered_data = df_histogram[df_histogram['disease'] == disease]

    grouped = filtered_data.groupby('patient_age')['duration'].mean()
    stats = grouped.describe().reset_index()
    stats.columns = ['Statistic', 'Value']
    return stats

# Initialize statistics table for histogram
histogram_stats = prepare_histogram_statistics("All")
source_histogram_stats = ColumnDataSource(histogram_stats)

# Table for Histogram Statistics
columns_histogram_stats = [
    TableColumn(field="Statistic", title="Statistic"),
    TableColumn(field="Value", title="Value")
]
table_histogram_stats = DataTable(
    source=source_histogram_stats,
    columns=columns_histogram_stats,
    height=300,
    width=400
)

# Callback Function for Histogram and Stats Update
def update_histogram(attr, old, new):
    selected_disease = histogram_disease_dropdown.value

    # Update histogram plot data
    updated_histogram_data = prepare_histogram_data(selected_disease)
    source_histogram.data = updated_histogram_data

    # Update statistics table
    updated_histogram_stats = prepare_histogram_statistics(selected_disease)
    source_histogram_stats.data = updated_histogram_stats


histogram_disease_dropdown.on_change("value", update_histogram)

df_heatmap = get_experience_dataframe()
source_heatmap = ColumnDataSource(df_heatmap)

# Heatmap Visualization
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

# Add Rectangles for Heatmap
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

# Add HoverTool
hover = HoverTool(
    tooltips=[
        ("Experience", "@experience_category"),
        ("Appointments", "@appointment_category"),
        ("Doctors", "@doctor_count")
    ]
)
heatmap_chart.add_tools(hover)

# Add Color Bar
color_bar = ColorBar(
    color_mapper=color_mapper['transform'],
    width=8,
    location=(0, 0),
    title="Number of Doctors"
)
heatmap_chart.add_layout(color_bar, 'right')

# Statistics Table
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


df_linear = get_disease_history_seasons_dataframe()
df_linear['year'] = df_linear['start_of_disease'].dt.year

# Initial data
initial_year = df_linear['year'].min()
initial_disease = df_linear['disease'].iloc[0]

# Data filtering function
def filter_data(year, disease):
    filtered = df_linear[(df_linear['year'] == year) & (df_linear['disease'] == disease)]
    # Count occurrences for each month (ensure all months are included)
    monthly_counts = (
        filtered.groupby('start_month')
        .size()
        .reindex(range(1, 13), fill_value=0)  # Ensure all months (1-12) are included
        .reset_index(name='count')
    )
    monthly_counts = monthly_counts.rename(columns={'start_month': 'month'})
    monthly_counts['month'] = monthly_counts['month'].apply(lambda x: datetime(1900, x, 1).strftime('%B'))
    return monthly_counts

# Initial filtered data
filtered_data = filter_data(initial_year, initial_disease)

# Data sources
source_line = ColumnDataSource(filtered_data)
source_table = ColumnDataSource(filtered_data.describe().reset_index().rename(columns={'index': 'Statistic'}))

# Line plot
line_plot = figure(
    title="Disease Occurrences by Month",
    x_range=filtered_data['month'],
    height=400,
    width=800,
    tools="pan, wheel_zoom, box_zoom, reset",
    toolbar_location="above"
)

line_plot.line(x='month', y='count', source=source_line, line_width=2, color="navy", legend_label="Occurrences")
line_plot.circle(x='month', y='count', source=source_line, size=8, color="orange")
line_plot.xaxis.axis_label = "Month"
line_plot.yaxis.axis_label = "Occurrences"
line_plot.legend.location = "top_left"

# Statistics table
columns_table = [
    TableColumn(field="Statistic", title="Statistic"),
    TableColumn(field="count", title="Value"),
]
stats_table = DataTable(source=source_table, columns=columns_table, height=300, width=400)

# Dropdown and Slider
diseases = sorted(df_linear['disease'].unique())
years = sorted(df_linear['year'].unique())

disease_dropdown = Select(title="Select Disease", value=initial_disease, options=diseases)
year_slider = Slider(title="Select Year", value=initial_year, start=years[0], end=years[-1], step=1)

# Update function
def update(attr, old, new):
    selected_disease = disease_dropdown.value
    selected_year = year_slider.value
    new_filtered_data = filter_data(selected_year, selected_disease)
    source_line.data = ColumnDataSource.from_df(new_filtered_data)
    new_stats = new_filtered_data['count'].describe().reset_index().rename(columns={'index': 'Statistic', 0: 'Value'})
    source_table.data = ColumnDataSource.from_df(new_stats)

# Add event listeners
disease_dropdown.on_change('value', update)
year_slider.on_change('value', update)

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

# Layout
layout = column(
    row(pie_chart, table_pie),
    row(disease_dropdown, map_chart, table_map),
    row(histogram_disease_dropdown, histogram_chart, table_histogram_stats),
    row(heatmap_chart, table_heatmap_stats),
    row(disease_dropdown, year_slider),
    row(line_plot, stats_table),
    row(concurrency, concurrency_table)
)

# Add to Document
curdoc().add_root(layout)
curdoc().title = "Bokeh Dashboard"
