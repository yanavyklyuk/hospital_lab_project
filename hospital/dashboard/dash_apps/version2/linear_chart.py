from datetime import datetime
from bokeh.models import (Select, Slider, ColumnDataSource, DataTable, TableColumn)
from bokeh.plotting import figure

from linear_chart_data import get_disease_history_seasons_dataframe


def create_linear_chart():
    df_linear = get_disease_history_seasons_dataframe()
    df_linear['year'] = df_linear['start_of_disease'].dt.year

    initial_year = df_linear['year'].min()
    initial_disease = df_linear['disease'].iloc[0]

    def filter_data(year, disease):
        filtered = df_linear[(df_linear['year'] == year) & (df_linear['disease'] == disease)]
        monthly_counts = (
            filtered.groupby('start_month')
            .size()
            .reindex(range(1, 13), fill_value=0)
            .reset_index(name='count')
        )
        monthly_counts = monthly_counts.rename(columns={'start_month': 'month'})
        monthly_counts['month'] = monthly_counts['month'].apply(lambda x: datetime(1900, x, 1).strftime('%B'))
        return monthly_counts

    filtered_data = filter_data(initial_year, initial_disease)

    source_line = ColumnDataSource(filtered_data)
    source_table = ColumnDataSource(filtered_data.describe().reset_index().rename(columns={'index': 'Statistic'}))

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

    columns_table = [
        TableColumn(field="Statistic", title="Statistic"),
        TableColumn(field="count", title="Value"),
    ]
    stats_table = DataTable(source=source_table, columns=columns_table, height=300, width=400)

    diseases = sorted(df_linear['disease'].unique())
    years = sorted(df_linear['year'].unique())

    disease_dropdown = Select(title="Select Disease", value=initial_disease, options=diseases)
    year_slider = Slider(title="Select Year", value=initial_year, start=years[0], end=years[-1], step=1)

    return line_plot, stats_table, disease_dropdown, year_slider, source_line, source_table, filter_data
