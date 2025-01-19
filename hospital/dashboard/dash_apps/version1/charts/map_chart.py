import plotly.express as px

def preprocess_data(df):
    if 'patient_country' not in df.columns:
        raise ValueError("DataFrame does not contain the required column 'patient_country'.")
    country_counts = df['patient_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Cases']
    return country_counts

def create_map_chart(df):

    country_counts = preprocess_data(df)

    country_counts['Cases'] = country_counts['Cases'].replace(0, None)

    fig = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Cases",
        hover_name="Country",
        color_continuous_scale="Hot_r",
        range_color=[1, max(country_counts['Cases'].dropna())],
        labels={'Cases': 'Number of Cases'},
        title="Global Disease Cases"
    )

    fig.update_geos(
        scope="europe",
        visible=True,
        showcoastlines=True,
        coastlinecolor="Black",
        projection_type="natural earth",
        showland=True,
        landcolor="lightgrey"
    )

    fig.update_traces(
        hovertemplate="<b>Country:</b> %{location}<br><b>Cases:</b> %{z}<extra></extra>",
    )

    return fig

def describe_to_table_map(df):
    if df.empty:
        return []

    df = preprocess_data(df)

    description = df.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data