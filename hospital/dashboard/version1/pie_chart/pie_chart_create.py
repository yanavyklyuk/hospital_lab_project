import plotly.express as px

def create_pie_chart(df):
    fig = px.pie(df, values = 'cost', names = 'name', title = 'Hospital income')
    return fig