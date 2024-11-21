from bokeh.layouts import column, row
from bokeh.models import (Select, Slider, ColumnDataSource, DataTable, TableColumn, HoverTool, PanTool, WheelZoomTool, BoxZoomTool,
                          ResetTool, GeoJSONDataSource, ColorBar)
from bokeh.plotting import curdoc, figure
import numpy as np
import pandas as pd
import json
import requests
from bokeh.palettes import Category20c, Viridis256
from bokeh.transform import linear_cmap

from pie_chart_data import get_appointments
from map_chart_data import get_disease_histories, get_diseases
from histogram_chart_data import get_disease_histories_h
from heatmap_chart_data import get_experience_dataframe
from linear_chart_data import get_disease_history_seasons_dataframe

# Data Preparation
df_pie = get_appointments()
df_map = get_disease_histories()
#df_histogram = get_disease_histories_h()
##df_heatmap = get_experience_dataframe()
#df_linear = get_disease_history_seasons_dataframe()

# ColumnDataSource Initialization
#source_hist = ColumnDataSource(df_histogram)
#source_heatmap = ColumnDataSource(df_heatmap)
#source_linear = ColumnDataSource(df_linear)

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
year_slider = Slider(start=2015, end=2025, value=2020, step=1, title="Select Year")

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

# Layout
layout = column(
    row(pie_chart, table_pie),
    row(disease_dropdown, map_chart, table_map),
    #row(linear_chart, table_heatmap),
    #year_slider
)

# Add to Document
curdoc().add_root(layout)
curdoc().title = "Bokeh Dashboard"
