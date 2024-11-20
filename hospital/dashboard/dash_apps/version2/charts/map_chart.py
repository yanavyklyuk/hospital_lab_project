from bokeh.plotting import figure, show
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, ColumnDataSource, TableColumn, DataTable
from bokeh.palettes import Reds
from bokeh.io import output_notebook
from bokeh.layouts import column
import pandas as pd
import geopandas as gpd

# Preprocess Data
def preprocess_data(df):
    if 'patient_country' not in df.columns:
        raise ValueError("DataFrame does not contain the required column 'patient_country'.")
    country_counts = df['patient_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Cases']
    return country_counts

# Load GeoJSON data for countries
def load_geojson():
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    geo_df = gpd.read_file(url)
    return geo_df

# Merge data with GeoJSON
def merge_data(geo_df, data):
    geo_df = geo_df.merge(data, how='left', left_on='name', right_on='Country')
    geo_df['Cases'] = geo_df['Cases'].fillna(0)  # Replace NaN cases with 0
    return geo_df

# Create Choropleth Map
def create_map_chart_bokeh(df):
    country_counts = preprocess_data(df)
    geo_df = load_geojson()
    merged_geo = merge_data(geo_df, country_counts)

    # Convert GeoDataFrame to GeoJSON
    geo_source = GeoJSONDataSource(geojson=merged_geo.to_json())

    # Create a color mapper
    mapper = LinearColorMapper(
        palette=Reds[256],
        low=0,
        high=country_counts['Cases'].max()
    )

    # Create figure
    p = figure(
        title="Global Disease Cases",
        width=800,
        height=500,
        toolbar_location="below",
        tooltips=[("Country", "@Country"), ("Cases", "@Cases")],
    )

    # Add patches for countries
    p.patches(
        "xs",
        "ys",
        source=geo_source,
        fill_color={'field': 'Cases', 'transform': mapper},
        line_color="gray",
        line_width=0.5,
        fill_alpha=0.7
    )

    # Add color bar
    color_bar = ColorBar(
        color_mapper=mapper,
        label_standoff=12,
        location=(0, 0),
        title="Number of Cases"
    )
    p.add_layout(color_bar, 'right')

    return p

# Create Summary Table
def describe_to_table_map_bokeh(df):
    if df.empty:
        return None

    df = preprocess_data(df)

    description = df.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    # Convert to Bokeh DataTable
    source = ColumnDataSource(description_reset)
    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]
    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table