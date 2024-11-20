from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.layouts import column
import pandas as pd

# Function to group data by start_month
def group_df(df):
    grouped_df = (
        df
        .groupby('start_month')
        .size()
        .reset_index(name='disease_count')
    )
    return grouped_df

# Create the line chart
def create_linear_chart_bokeh(df):
    grouped_df = group_df(df)

    # Ensure all months are included, even with 0 count
    full_months = pd.DataFrame({'start_month': range(1, 13)})
    grouped_df = full_months.merge(grouped_df, on='start_month', how='left').fillna(0)
    grouped_df['disease_count'] = grouped_df['disease_count'].astype(int)

    # Map month numbers to names for x-axis labels
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    grouped_df['month_name'] = grouped_df['start_month'].apply(lambda x: month_names[x - 1])

    source = ColumnDataSource(grouped_df)

    # Create the figure
    p = figure(
        title="Disease Trends for Disease in Year",
        x_axis_label="Month",
        y_axis_label="Disease Count",
        x_range=month_names,  # Ensure proper categorical x-axis
        width=800,
        height=400,
        tooltips=[("Month", "@month_name"), ("Disease Count", "@disease_count")],
    )

    # Add a line and markers
    p.line(x="month_name", y="disease_count", source=source, line_width=2, color="blue", legend_label="Disease Count")
    p.circle(x="month_name", y="disease_count", source=source, size=8, color="red")

    p.legend.location = "top_left"

    return p

# Create a descriptive table
def describe_to_table_lin_bokeh(df):
    if df.empty:
        return None

    df = group_df(df)

    # Calculate descriptive statistics
    description = df.describe()
    description_reset = description.reset_index()
    description_reset.columns = ['Statistic'] + list(description.columns)

    # Convert to Bokeh DataTable
    source = ColumnDataSource(description_reset)
    columns = [TableColumn(field=col, title=col) for col in description_reset.columns]
    data_table = DataTable(source=source, columns=columns, width=800, height=300)

    return data_table