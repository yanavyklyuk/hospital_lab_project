from bokeh.models import (Select, ColumnDataSource, DataTable, TableColumn, HoverTool)
from bokeh.plotting import figure
from histogram_chart_data import get_disease_histories_h


df_histogram = get_disease_histories_h()


def prepare_histogram_data(disease):
    if disease == "All":
        filtered_data = df_histogram
    else:
        filtered_data = df_histogram[df_histogram['disease'] == disease]

    grouped = filtered_data.groupby('patient_age')['duration'].mean().reset_index()
    grouped.columns = ['patient_age', 'avg_duration']
    return grouped


def prepare_histogram_statistics(disease):
    if disease == "All":
        filtered_data = df_histogram
    else:
        filtered_data = df_histogram[df_histogram['disease'] == disease]

    grouped = filtered_data.groupby('patient_age')['duration'].mean()
    stats = grouped.describe().reset_index()
    stats.columns = ['Statistic', 'Value']
    return stats


def create_histogram_chart():

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

    histogram_stats = prepare_histogram_statistics("All")
    source_histogram_stats = ColumnDataSource(histogram_stats)

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

    return histogram_chart, histogram_disease_dropdown, table_histogram_stats, source_histogram, source_histogram_stats
