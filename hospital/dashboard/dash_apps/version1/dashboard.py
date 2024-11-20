from dash import dcc
from dash import html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from ..data.pie_chart_data import get_appointments
from ..data.map_chart_data import get_disease_histories, get_diseases
from ..data.histogram_chart_data import get_disease_histories_h, get_diseases_h
from .charts.pie_chart import create_pie_chart, describe_to_table
from .charts.map_chart import create_map_chart, describe_to_table_map
from .charts.histogram_chart import create_histogram_chart, describe_to_table_hist

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
                    html.H4('Disease duration statistics', style={'textAlign': 'center'}),
                    DataTable(
                        id='describe-table-hist',
                        style_table={'height': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        columns=[
                            {'name': 'Statistic', 'id': 'Statistic'},
                            {'name': 'Values', 'id': 'duration'}
                        ],
                        data=[]
                    )
                ]
            ),

            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    dcc.Dropdown(
                        id='disease-dropdown-histogram',
                        options=[],
                        value=None,
                        clearable=False,
                        placeholder="All"
                    ),
                    dcc.Graph(id='histogram-chart', animate=True)
                ]
            ),


        ]
    ),
])


@app.callback(
    [Output('pie-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('disease-dropdown', 'options'),
     Output('describe-table', 'data'),
     Output('describe-table-map', 'data'),
     Output('describe-table-hist', 'data'),
     Output('histogram-chart', 'figure'),
     Output('disease-dropdown-histogram', 'options')],
    [
        Input('disease-dropdown', 'value'),
        Input('disease-dropdown-histogram', 'value')]
)
def update_graphs(selected_disease, selected_disease_histogram):
    df_pie = get_appointments()
    df_map = get_disease_histories()
    df_histogram = get_disease_histories_h()

    disease_options = get_diseases(df_map)

    if selected_disease:
        df_map_filtered = df_map[df_map['disease'] == selected_disease]
    else:
        df_map_filtered = df_map

    disease_options_h = get_diseases_h(df_histogram)

    if selected_disease_histogram:
        df_hist_filtered = df_histogram[df_histogram['disease'] == selected_disease_histogram]
    else:
        df_hist_filtered = df_histogram

    pie_chart = create_pie_chart(df_pie)
    map_chart = create_map_chart(df_map_filtered)
    histogram_chart = create_histogram_chart(df_hist_filtered)

    table_data = describe_to_table(df_pie[['favor_cost']])
    table_data_map = describe_to_table_map(df_map_filtered)
    table_data_hist = describe_to_table_hist(df_hist_filtered)

    return (pie_chart, map_chart, disease_options, table_data, table_data_map, table_data_hist,
            histogram_chart, disease_options_h)
