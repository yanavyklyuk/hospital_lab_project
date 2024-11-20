import plotly.express as px
import pandas as pd

def create_bubble_chart(df):

    fig = px.scatter_3d(
        df,
        x="threads",
        y="processes",
        z="time",
        size="time",
        color="time",
        title="3D Concurrency Analysis: Processes vs Threads vs Time",
        labels={
            "threads": "Number of Threads",
            "processes": "Number of Processes",
            "time": "Execution Time (s)"
        },
        template="plotly_white",
    )
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="Number of Threads"
            ),
            yaxis=dict(
                title="Number of Processes",
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
            zaxis=dict(
                title="Execution Time (s)",
            ),
        ),
        coloraxis_colorbar=dict(title="Execution Time (s)"),
    )

    return fig


def describe_to_table_bubble(df):
    if df.empty:
        return []

    if isinstance(df, pd.Series):
        df = df.to_frame(name=df.name if df.name else 'value')

    description = df.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data
