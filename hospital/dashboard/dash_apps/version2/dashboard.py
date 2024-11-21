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

from concurrency_chart import create_concurrency_graph
from linear_chart import create_linear_chart
from heatmap_chart import create_heatmap_chart
from histogram_chart import create_histogram_chart, prepare_histogram_data, prepare_histogram_statistics
from pie_chart import create_pie_chart
from map_chart import convert_geojson_types, preprocess_data, create_map_chart


df_map, map_chart, table_map, disease_dropdown_map, geo_source, color_bar, source_stats_map = create_map_chart()


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


disease_dropdown_map.on_change("value", update_map)



pie_chart, table_pie = create_pie_chart()

(histogram_chart, histogram_disease_dropdown, table_histogram_stats, source_histogram,
 source_histogram_stats) = create_histogram_chart()


def update_histogram(attr, old, new):
    selected_disease = histogram_disease_dropdown.value

    # Update histogram plot data
    updated_histogram_data = prepare_histogram_data(selected_disease)
    source_histogram.data = updated_histogram_data

    # Update statistics table
    updated_histogram_stats = prepare_histogram_statistics(selected_disease)
    source_histogram_stats.data = updated_histogram_stats


histogram_disease_dropdown.on_change("value", update_histogram)

heatmap_chart, table_heatmap_stats = create_heatmap_chart()

(line_plot, line_table, disease_dropdown, year_slider, source_line, source_line_table,
 filter_data) = create_linear_chart()


def update_line_plot(attr, old, new):
    selected_disease = disease_dropdown.value
    selected_year = year_slider.value
    new_filtered_data = filter_data(selected_year, selected_disease)
    source_line.data = ColumnDataSource.from_df(new_filtered_data)
    new_stats = new_filtered_data['count'].describe().reset_index().rename(columns={'index': 'Statistic', 0: 'Value'})
    source_line_table.data = ColumnDataSource.from_df(new_stats)


disease_dropdown.on_change('value', update_line_plot)
year_slider.on_change('value', update_line_plot)

concurrency, concurrency_table = create_concurrency_graph()

# Layout
layout = column(
    row(pie_chart, table_pie),
    row(disease_dropdown_map, map_chart, table_map),
    row(histogram_disease_dropdown, histogram_chart, table_histogram_stats),
    row(heatmap_chart, table_heatmap_stats),
    row(disease_dropdown, year_slider),
    row(line_plot, line_table),
    row(concurrency, concurrency_table)
)

# Add to Document
curdoc().add_root(layout)
curdoc().title = "Bokeh Dashboard"
