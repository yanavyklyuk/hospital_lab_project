from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.layouts import column
import pandas as pd
import numpy as np

# Create a pie chart
def create_pie_chart_bokeh(df):
    df['angle'] = df['favor_cost'] / df['favor_cost'].sum() * 2 * np.pi  # Calculate angles for the pie chart
    df['color'] = Category20c[len(df)]  # Assign colors from a palette

    source = ColumnDataSource(df)

    p = figure(
        title="Hospital Income",
        height=400,
        width=400,
        toolbar_location=None,
        tools="hover",
        tooltips=[("Favor", "@favor_name"), ("Total Income", "@favor_cost")],
        x_range=(-0.5, 1.0),
    )

    # Add wedges
    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white",
        fill_color='color',
        legend_field='favor_name',
        source=source,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.legend.title = "Favor"
    p.legend.location = "top_right"

    return p

# Create a descriptive table
def describe_to_table_bokeh(df):
    if df.empty:
        return None

    # Calculate descriptive statistics
    description = df.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    # Convert to Bokeh DataTable
    source = ColumnDataSource(description_reset)
    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]
    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table