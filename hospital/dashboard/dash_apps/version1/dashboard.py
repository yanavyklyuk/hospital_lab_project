from dash import dcc
from dash import html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from ..data.pie_chart_data import get_appointments, describe_to_table
from ..data.map_chart_data import get_disease_histories, get_diseases
from .charts.pie_chart import create_pie_chart
from .charts.map_chart import create_map_chart, describe_to_table_map

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Dashboard', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Statistics', style={'textAlign': 'center', 'marginBottom': '40px'}),
    html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'padding': '20px'
        },
        children=[
            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    dcc.Graph(id='pie-chart', animate=True)
                ]
            ),

            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    html.H4('Favor income statistics', style={'textAlign': 'center'}),
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

html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'padding': '20px'
        },
        children=[
            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    dcc.Dropdown(
                        id='disease-dropdown',
                        options=[],
                        value=None,
                        clearable=False,
                        placeholder="All"
                    ),
                    dcc.Graph(id='map-chart', animate=True)
                ]
            ),

            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    html.H4('Disease statistics', style={'textAlign': 'center'}),
                    DataTable(
                        id='describe-table-map',
                        style_table={'height': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        columns=[
                            {'name': 'Statistic', 'id': 'Statistic'},
                            {'name': 'Values', 'id': 'Cases'}
                        ],
                        data=[]
                    )
                ]
            )
        ]
    ),
])


@app.callback(
    [Output('pie-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('disease-dropdown', 'options'),
     Output('describe-table', 'data'),
     Output('describe-table-map', 'data')],
    [
     Input('disease-dropdown', 'value')]
)
def update_graphs(selected_disease):
    df = get_appointments()
    df2 = get_disease_histories()

    disease_options = get_diseases(df2)
    if selected_disease:
        df2_filtered = df2[df2['disease'] == selected_disease]
    else:
        df2_filtered = df2

    graph = create_pie_chart(df)

    map_chart = create_map_chart(df2_filtered)

    table_data = describe_to_table(df[['favor_cost']])
    table_data_map = describe_to_table_map(df2_filtered)

    return graph, map_chart, disease_options, table_data, table_data_map
