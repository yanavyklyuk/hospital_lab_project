from bokeh.models import (Select, ColumnDataSource, DataTable, TableColumn, HoverTool, GeoJSONDataSource, ColorBar)
from bokeh.plotting import figure
import numpy as np
import pandas as pd
import json
import requests
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap

from map_chart_data import get_disease_histories, get_diseases


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


def create_map_chart():
    df_map = get_disease_histories()

    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    response = requests.get(url)
    if response.status_code == 200:
        geojson_data = response.json()
    else:
        raise ValueError(f"Failed to fetch GeoJSON: {response.status_code}")

    # GeoJSONDataSource
    geo_source = GeoJSONDataSource(geojson=json.dumps(geojson_data))




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

    return df_map, map_chart, table_map, disease_dropdown, geo_source, color_bar, source_stats_map