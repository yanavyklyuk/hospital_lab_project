from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from .pie_chart.pie_chart_view import get_appointments
from .pie_chart.pie_chart_create import create_pie_chart

app = DjangoDash('Dashboard')

app.layout = html.Div(
    style={'width': '100%', 'height': '100000vh', 'display': 'flex', 'flexDirection': 'column'},  # Встановлюємо максимальний розмір
    children = [
    html.H1('Dashboard'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='pie-chart'),
        ], className='six columns'),
    ], className='row'),

])

@app.callback(
    [Output('pie-chart', 'figure')],
    [Input('pie-chart', 'id')]
)
def update_graphs(n):
    df = get_appointments()
    fig1 = create_pie_chart(df)


    return [fig1]
