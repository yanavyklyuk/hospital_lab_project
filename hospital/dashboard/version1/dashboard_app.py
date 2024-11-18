from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.dash_table import DataTable
from django_plotly_dash import DjangoDash
from dashboard.version1.charts.pie_chart import get_appointments, create_pie_chart, describe_to_table

app = DjangoDash('Dashboard')

app.layout = html.Div(
    style={'width': '100%', 'height': '100vh', 'display': 'flex', 'flexDirection': 'column'},  # Встановлюємо максимальний розмір
    children=[
        html.H1('Dashboard'),

        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between'},
            children=[
                html.Div(
                    style={'width': '60%'},
                    children=[dcc.Graph(id='pie-chart')]
                ),

                html.Div(
                    style={'width': '35%'},
                    children=[
                        html.H4('Favor cost statistics'),
                        DataTable(
                            id='describe-table',
                            style_table={'height': '400px', 'overflowY': 'auto'},
                            style_cell={'textAlign': 'center', 'padding': '10px'},
                            columns=[
                                {'name': 'Statistic', 'id': 'Statistic'},
                                {'name': 'Values', 'id': 'favor_cost'}
                            ],
                            data=[]
                        )
                    ]
                )
            ]
        ),
    ]
)

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('describe-table', 'data')],
    [Input('pie-chart', 'id')]
)
def update_graphs(n):
    df = get_appointments()
    fig1 = create_pie_chart(df)
    table_data = describe_to_table(df[['favor_cost']])
    print(table_data)

    return [fig1, table_data]
