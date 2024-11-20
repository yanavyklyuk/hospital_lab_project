import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dataframes import get_experience_dataframe, get_disease_history_seasons_dataframe


df_1 = get_experience_dataframe('4948ee5037d704266422e96e6c3cf83fb76527bf')
df_2 = get_disease_history_seasons_dataframe('4948ee5037d704266422e96e6c3cf83fb76527bf')
df_3 = pd.read_csv("concurrency_analysis.csv")

fig = px.imshow(
    df_1.pivot_table(index='appointment_category', columns='experience_category', values='doctor_count', fill_value=0),
    labels=dict(x="Doctor Experience (years)", y="Appointment Count Category"),
    color_continuous_scale='Viridis',
    title="Number of Doctors by Experience and Appointment Count"
)

fig.update_layout(
    xaxis_title="Doctor Experience (years)",
    yaxis_title="Appointment Count Category",
    coloraxis_colorbar=dict(title="Number of Doctors"),
    template="plotly_white",
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3],
        ticktext=["0-5 years", "5-10 years", "10-15 years", "15+ years"]
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["0-5", "5-10", "10-20", "20-30", "30+"],
    )
)

fig_parallel = px.scatter_3d(
    df_3,
    x="threads",  # Кількість потоків на осі X
    y="processes",  # Кількість процесів на осі Y
    z="time",  # Час виконання на осі Z
    size="time",  # Розмір бульбашок залежить від часу
    color="time",  # Колір залежить від часу виконання
    title="3D Concurrency Analysis: Processes vs Threads vs Time",
    labels={
        "threads": "Number of Threads",
        "processes": "Number of Processes",
        "time": "Execution Time (s)"
    },
    template="plotly_white",
)
fig_parallel.update_layout(
    scene=dict(
        xaxis=dict(
            title="Number of Threads"
        ),
        yaxis=dict(
            title="Number of Processes",
            tickmode='array',  # Встановлення міток лише для цілих чисел
            tickvals=[1, 2, 3, 4, 5],  # Тільки цілі значення для кількості потоків
            ticktext=["1", "2", "3", "4", "5"]
        ),
        zaxis=dict(
            title="Execution Time (s)",
        ),
    ),
    coloraxis_colorbar=dict(title="Execution Time (s)"),
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard"),
    html.Label("Choose disease:"),
    dcc.Dropdown(
        id='disease-dropdown',
        options=[{'label': i, 'value': i} for i in df_2['disease'].unique()],
        value='Alzheimer Disease'
    ),
    html.Label("Choose year:"),
    dcc.Slider(
        id='year-slider',
        min=df_2['start_of_disease'].min().year,
        max=df_2['start_of_disease'].max().year,
        value=df_2['start_of_disease'].min().year,
        marks={str(year): str(year) for year in df_2['start_of_disease'].unique().year},
        step=None
    ),
    html.Label("Doctors by Experience and Appointment Count"),
    dcc.Graph(id='heatmap', figure=fig),
    html.Label("Disease History Seasons"),
    dcc.Graph(id='seasons-linear'),
    html.H1("Concurrency Analysis Dashboard", style={"textAlign": "center"}),
    dcc.Graph(id="3d-bubble-chart", figure=fig_parallel,)
])

@app.callback(
    Output('seasons-linear', 'figure'),
    [Input('disease-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graphs(disease, year):
    filtered_df = df_2[
        (df_2['disease'] == disease) & (df_2['start_of_disease'].dt.year == year)
        ]

    grouped_df = (
        filtered_df
        .groupby('start_month')
        .size()
        .reset_index(name='disease_count')
    )

    full_months = pd.DataFrame({'start_month': range(1, 13)})
    grouped_df = full_months.merge(grouped_df, on='start_month', how='left').fillna(0)

    grouped_df['disease_count'] = grouped_df['disease_count'].astype(int)

    fig = px.line(
        grouped_df,
        x='start_month',
        y='disease_count',
        title=f"Disease Trends for {disease} in {year}",
        labels={
            "start_month": "Month",
            "disease_count": "Disease Count"
        }
    )

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
        ),
        yaxis=dict(
            title="Number of Diseases",
            rangemode="tozero"
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
