from dash import dcc
from dash import html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd

from .charts.heatmap_chart import create_heatmap_chart
from ..data.pie_chart_data import get_appointments
from ..data.map_chart_data import get_disease_histories, get_diseases
from ..data.histogram_chart_data import get_disease_histories_h, get_diseases_h
from ..data.heatmap_chart_data import get_experience_dataframe
from ..data.linear_chart_data import get_disease_history_seasons_dataframe, get_diseases_l, get_years_l
from .charts.pie_chart import create_pie_chart, describe_to_table
from .charts.map_chart import create_map_chart, describe_to_table_map
from .charts.histogram_chart import create_histogram_chart, describe_to_table_hist
from .charts.heatmap_chart import create_heatmap_chart, describe_to_table_heat
from .charts.linear_chart import create_linear_chart, describe_to_table_lin
from .charts.bubble_chart import create_bubble_chart, describe_to_table_bubble
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "concurrency_analysis.csv")
df_bubble = pd.read_csv(file_path)

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
                    dcc.Graph(id='heatmap-chart', animate=True),
                ]
            ),
            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    html.H4('Doctors Appointments Statistics', style={'textAlign': 'center'}),
                    DataTable(
                        id='describe-table-heat',
                        style_table={'height': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        columns=[
                            {'name': 'Statistic', 'id': 'Statistic'},
                            {'name': 'Values', 'id': 'doctor_count'}
                        ],
                        data=[]
                    )
                ]
            ),
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
                        id='disease-dropdown-linear',
                        options=[],
                        value='Alzheimer Disease',
                        clearable=False,
                    ),
                    html.Div(
                        style={'marginTop': '20px'},
                        children=[
                            dcc.Slider(
                                id='year-slider',
                                min=None,
                                max=None,
                                value=None,
                                marks={},
                                step=1
                            )
                        ]
                    ),
                    dcc.Graph(id='linear-chart', animate=True)
                ]
            ),

            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    html.H4('Disease History Seasons', style={'textAlign': 'center'}),
                    DataTable(
                        id='describe-table-lin',
                        style_table={'height': '400px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        columns=[
                            {'name': 'Statistic', 'id': 'Statistic'},
                            {'name': 'Values', 'id': 'disease_count'}
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
                    dcc.Graph(id='bubble-chart', animate=True)
                ]
            ),

            html.Div(
                style={'flex': '1', 'marginRight': '20px'},
                children=[
                    html.H4('Concurrent Querying', style={'textAlign': 'center'}),
                    DataTable(
                        id='describe-table-bubble',
                        style_table={'height': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        columns=[
                            {'name': 'Statistic', 'id': 'Statistic'},
                            {'name': 'Values', 'id': 'time'}
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
     Output('describe-table-map', 'data'),
     Output('describe-table-hist', 'data'),
     Output('histogram-chart', 'figure'),
     Output('disease-dropdown-histogram', 'options'),
     Output('heatmap-chart', 'figure'),
     Output('describe-table-heat', 'data'),
     Output('linear-chart', 'figure'),
     Output('disease-dropdown-linear', 'options'),
     Output('year-slider', 'min'),
     Output('year-slider', 'max'),
     Output('year-slider', 'value'),
     Output('year-slider', 'marks'),
     Output('describe-table-lin', 'data'),
     Output('bubble-chart', 'figure'),
     Output('describe-table-bubble', 'data'),
     ],
    [
        Input('disease-dropdown', 'value'),
        Input('disease-dropdown-histogram', 'value'),
        Input('disease-dropdown-linear', 'value'),
        Input('year-slider', 'value')]
)
def update_graphs(selected_disease, selected_disease_histogram, selected_disease_l, selected_year):
    df_pie = get_appointments()
    df_map = get_disease_histories()
    df_histogram = get_disease_histories_h()
    df_heatmap = get_experience_dataframe()
    df_linear = get_disease_history_seasons_dataframe()

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

    disease_options_l = get_diseases_l(df_linear)
    years = df_linear['start_of_disease'].dt.year.unique()
    year_min, year_max = years.min(), years.max()
    year_marks = {int(year): str(year) for year in years}

    if selected_year is None:
        selected_year = year_min

    if selected_disease_l:
        df_lin_filtered = df_linear[
            (df_linear['disease'] == selected_disease_l) & (df_linear['start_of_disease'].dt.year == selected_year)
            ]
    else:
        df_lin_filtered = df_linear

    pie_chart = create_pie_chart(df_pie)
    map_chart = create_map_chart(df_map_filtered)
    histogram_chart = create_histogram_chart(df_hist_filtered)
    heatmap_chart = create_heatmap_chart(df_heatmap)
    linear_chart = create_linear_chart(df_lin_filtered)
    bubble_chart = create_bubble_chart(df_bubble)

    table_data = describe_to_table(df_pie[['favor_cost']])
    table_data_map = describe_to_table_map(df_map_filtered)
    table_data_hist = describe_to_table_hist(df_hist_filtered)
    table_data_heat = describe_to_table_heat(df_heatmap[['doctor_count']])
    table_data_lin = describe_to_table_lin(df_lin_filtered)
    table_data_bubble = describe_to_table_bubble(df_bubble['time'])

    return (pie_chart, map_chart, disease_options, table_data, table_data_map, table_data_hist,
            histogram_chart, disease_options_h, heatmap_chart, table_data_heat, linear_chart,
            disease_options_l, year_min, year_max, selected_year, year_marks, table_data_lin, bubble_chart, table_data_bubble)
