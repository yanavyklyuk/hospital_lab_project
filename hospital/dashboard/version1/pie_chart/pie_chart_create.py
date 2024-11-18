import plotly.express as px

def create_pie_chart(df):
    fig = px.pie(df, values = 'favor_cost', names = 'favor_name', title = 'Hospital income')
    return fig