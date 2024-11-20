from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.io import output_notebook
from bokeh.layouts import column
import pandas as pd

# Function to calculate the average disease duration
def get_average_duration(df):
    avg_duration = df.groupby('patient_age')['duration'].mean().reset_index()
    return avg_duration

# Function to create a histogram (bar chart)
def create_histogram_chart_bokeh(df):
    df_avg_duration = get_average_duration(df)
    source = ColumnDataSource(df_avg_duration)

    # Create the figure
    p = figure(
        title="Average Disease Duration by Patient Age",
        x_axis_label="Age of Patient",
        y_axis_label="Average Duration (days)",
        x_range=list(map(str, df_avg_duration['patient_age'])),  # Ensure x-axis uses categorical range
        tooltips=[("Age", "@patient_age"), ("Avg Duration", "@duration{0.0}")],
        width=800,
        height=400
    )

    # Add vertical bars
    p.vbar(
        x="patient_age",
        top="duration",
        width=0.8,
        source=source,
        fill_color="skyblue",
        line_color="black"
    )

    return p

# Function to create a descriptive table
def describe_to_table_hist_bokeh(df):
    if df.empty:
        return None

    df_avg_duration = get_average_duration(df)

    # Calculate the description statistics
    description = df_avg_duration.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    # Create a ColumnDataSource for the table
    source = ColumnDataSource(description_reset)

    # Define columns for the DataTable
    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]

    # Create the DataTable
    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table