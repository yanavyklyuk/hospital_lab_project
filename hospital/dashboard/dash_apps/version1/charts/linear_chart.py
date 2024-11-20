import plotly.express as px
import pandas as pd

def group_df(df):
    grouped_df = (
        df
        .groupby('start_month')
        .size()
        .reset_index(name='disease_count')
    )

    return grouped_df

def create_linear_chart(df):
        grouped_df = group_df(df)
        full_months = pd.DataFrame({'start_month': range(1, 13)})
        grouped_df = full_months.merge(grouped_df, on='start_month', how='left').fillna(0)

        grouped_df['disease_count'] = grouped_df['disease_count'].astype(int)

        fig = px.line(
            grouped_df,
            x='start_month',
            y='disease_count',
            title=f"Disease Trends for disease in year",
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

def describe_to_table_lin(df):
    if df.empty:
        return []

    df = group_df(df)

    description = df.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data