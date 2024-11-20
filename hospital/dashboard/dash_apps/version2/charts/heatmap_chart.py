from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, DataTable, TableColumn
from bokeh.transform import factor_cmap
from bokeh.layouts import column
import pandas as pd

def create_heatmap_chart(df):
    # Prepare the pivoted data for the heatmap
    pivot_table = df.pivot_table(
        index='appointment_category',
        columns='experience_category',
        values='doctor_count',
        fill_value=0
    )

    # Convert the pivot table into a format suitable for Bokeh
    heatmap_data = pd.DataFrame(pivot_table.stack(), columns=["doctor_count"]).reset_index()
    source = ColumnDataSource(heatmap_data)

    # Define unique categories for axes
    x_categories = sorted(df['experience_category'].unique())
    y_categories = sorted(df['appointment_category'].unique(), reverse=True)

    # Create a linear color mapper for doctor count
    mapper = LinearColorMapper(
        palette="Viridis256",
        low=heatmap_data['doctor_count'].min(),
        high=heatmap_data['doctor_count'].max()
    )

    # Create the figure
    p = figure(
        title="Number of Doctors by Experience and Appointment Count",
        x_range=x_categories,
        y_range=y_categories,
        x_axis_label="Doctor Experience (years)",
        y_axis_label="Appointment Count Category",
        tooltips=[("Experience", "@experience_category"),
                  ("Appointment Category", "@appointment_category"),
                  ("Doctor Count", "@doctor_count")],
        width=800,
        height=600
    )

    # Draw the rectangles
    p.rect(
        x="experience_category",
        y="appointment_category",
        width=1,
        height=1,
        source=source,
        fill_color={'field': 'doctor_count', 'transform': mapper},
        line_color=None
    )

    # Add color bar
    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        title="Number of Doctors"
    )
    p.add_layout(color_bar, 'right')

    return p


def describe_to_table_heat(df):
    if df.empty:
        return None

    # Describe the DataFrame
    description = df.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    # Convert description into a ColumnDataSource
    source = ColumnDataSource(description_reset)

    # Create table columns
    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]

    # Create Bokeh DataTable
    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table