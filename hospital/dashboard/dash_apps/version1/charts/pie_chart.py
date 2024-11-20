import plotly.express as px

def create_pie_chart(df):
    fig = px.pie(
        df,
        values='favor_cost',
        names='favor_name',
        title='Hospital income',
        labels={
            'favor_name': 'Favor',
            'favor_cost': 'Total Income'
        }
    )

    fig.update_traces(
        hovertemplate="<b>Favor:</b> %{label}<br><b>Total Income:</b> %{value}<extra></extra>"
    )

    return fig