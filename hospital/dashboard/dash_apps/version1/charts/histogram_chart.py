import plotly.express as px

def get_average_duration(df):
    avg_duration = df.groupby('patient_age')['duration'].mean().reset_index()
    return avg_duration

def create_histogram_chart(df):
    df_avg_duration = get_average_duration(df)
    fig = px.bar(
        df_avg_duration,
        x='patient_age',
        y='duration',
        title='Average Disease Duration by Patient Age',
        labels={'patient_age': 'Age of Patient', 'duration': 'Average Duration (days)'},
        text='duration'
    )

    return fig

def describe_to_table_hist(df):
    if df.empty:
        return []

    df_avg_duration = get_average_duration(df)

    description = df_avg_duration.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data
