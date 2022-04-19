from dash import html
from .trends_callbacks import *
from pages.aggregate.data import news

# Controls ---------------------------------------------------------------------
controls = html.Div(
    id='aggregate-trends-controls',
    children=[
        html.H3("Options"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Tag Type"),
                dbc.Select(
                    id='aggregate-trends-tag-type',
                    options=[
                        {'label': 'Products', 'value': 'products'},
                        {'label': 'Markets', 'value': 'markets'},
                        {'label': 'Companies', 'value': 'companies'},
                        {'label': 'Keywords', 'value': 'keywords'},
                    ],
                    value='products',
                ),
            ]),
        ]),
    ]
)

trends_period_table = html.Div(
    children=[
        html.H5("Table"),
        dcc.Loading([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Metric"),
                    dbc.Select(
                        id='aggregate-trends-period-tbl-metric',
                        options=[
                            {'label': 'Frequency', 'value': 'frequency'},
                        ],
                        value='frequency',
                    ),
                ]),
            ], style={'width': '100%', 'display': 'none'}),
            dbc.Row([
                dbc.Col(
                    children=[
                        dbc.Button('Apply', id=f'aggregate-trends-period-tbl-apply', color="primary", className="mr-1", style={'display': 'none'}),
                    ]
                )
            ]),
            html.Br(),
            html.Br(),
            get_trends_table_frontend('aggregate-trends-period-tbl'),
            html.Button("Download CSV", id="aggregate-trends-period-download-btn"),
            dcc.Download(id="aggregate-trends-period-download-csv"),
        ]),
    ]
)

trends_period_timeseries = html.Div(
    children=[
        html.H5("Timeseries"),
        dcc.Loading([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Metric"),
                    dbc.Select(
                        id='aggregate-trends-period-timeseries-metric',
                        options=[
                            {'label': 'Frequency', 'value': 'frequency'},
                        ],
                        value='frequency',
                    ),
                ]),
                dbc.Col([
                    dbc.Label("Period"),
                    dbc.Select(
                        id='aggregate-trends-period-timeseries-period',
                        options=[
                            {'label': 'Monthly', 'value': 'monthly'},
                            {'label': 'Weekly', 'value': 'weekly'},
                            {'label': 'Daily', 'value': 'daily'},
                        ],
                        value='daily',
                    ),
                ]),
            ], style={'width': '100%'}),
            dbc.Row([
                dbc.Col(
                    children=[
                        dbc.Button('Apply', id=f'aggregate-trends-period-timeseries-apply', color="primary", className="mr-1"),
                    ]
                )
            ]),
            html.Br(),
            html.Br(),
            dcc.Graph(id='aggregate-trends-period-timeseries-graph', style={'zoom': '133.33%'}),
            dbc.Modal(
                id=f'aggregate-trends-period-timeseries-modal',
                size="lg",
                children=[
                    dbc.ModalHeader(id=f'aggregate-trends-period-timeseries-modal-header'),
                    dbc.ModalBody(
                        dt.DataTable(
                            id=f'aggregate-trends-period-timeseries-modal-table',
                            data=news(None).to_dict('records'),
                            columns=[{"name": i, "id": i, 'presentation': 'markdown'}
                                     for i in news(None).columns if i in ['Date', 'News Text', 'Source URL', 'External URL']],
                            # Style
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                            },
                            style_cell={
                                'font-family': 'Helvetica',
                                'font-size': '0.5rem',
                                'text-align': 'center',
                                'padding': '0.3rem',
                            },
                            # Functions
                            page_current=0, page_size=10,
                            sort_action='native',
                            sort_mode='multi',
                            # row_selectable='multi',
                            hidden_columns=['ID'],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                            persistence=True,
                            persistence_type='memory',
                            style_table={'overflowX': 'scroll'}
                        ),
                    ),
                ]
            ),
        ]),
    ]
)

trends_period = html.Div(
    id='aggregate-trends-period',
    children=[
        html.H3("Periodic Trends"),
        html.Br(),
        trends_period_table,
        html.Br(),
        trends_period_timeseries,
    ]
)

trends_compare = html.Div(
    id='aggregate-trends-compare',
    children=[
        html.H3("Compare Trends"),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Top"),
                    dbc.Input(id='aggregate-trends-compare-k', type="number", value=10, min=1, max=100, persistence=True, persistence_type='memory'),
                    dbc.InputGroupText("Tags"),
                ], size="sm", style={'width': '20%'}),
            ]),
        ]),
        html.Br(),
        dbc.Button("Apply", id="aggregate-trends-compare-apply", color="primary"),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H5('Trend 1'),
                dbc.InputGroup([
                    dbc.InputGroupText("Date From"),
                    dbc.Input(id='aggregate-trends-compare-1-start-date', type="date", value=(date.today() - timedelta(days=14)).strftime('%Y-%m-%d'), persistence=True, persistence_type='memory'),
                    dbc.InputGroupText("To"),
                    dbc.Input(id='aggregate-trends-compare-1-end-date', type="date", value=(date.today() - timedelta(days=7)).strftime('%Y-%m-%d'), persistence=True, persistence_type='memory'),
                ], size="sm", style={'width': '70%'}),
                html.Br(),
                get_trends_table_frontend('aggregate-trends-compare-1'),
                html.Button("Download CSV", id=f'aggregate-trends-compare-1-download-btn'),
                dcc.Download(id=f'aggregate-trends-compare-1-download'),

            ]),
            dbc.Col([
                html.H5('Trend 2'),
                dbc.InputGroup([
                    dbc.InputGroupText("Date From"),
                    dbc.Input(id='aggregate-trends-compare-2-start-date', type="date", value=(date.today() - timedelta(days=7)).strftime('%Y-%m-%d'), persistence=True, persistence_type='memory'),
                    dbc.InputGroupText("To"),
                    dbc.Input(id='aggregate-trends-compare-2-end-date', type="date", value=date.today().strftime('%Y-%m-%d'), persistence=True, persistence_type='memory'),
                ], size="sm", style={'width': '70%'}),
                html.Br(),
                get_trends_table_frontend('aggregate-trends-compare-2'),
                html.Button("Download CSV", id=f'aggregate-trends-compare-2-download-btn'),
                dcc.Download(id=f'aggregate-trends-compare-2-download'),
            ]),
        ]),
    ]
)


trends_alltime = html.Div(
    id='aggregate-trends-alltime',
    children=[
        html.H3("All Time Trends"),
        html.Br(),
        html.H5("Table"),
        dcc.Loading([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Metric"),
                    dbc.Select(
                        id='aggregate-trends-alltime-metric',
                        options=[
                            {'label': 'Frequency', 'value': 'frequency'},
                        ],
                        value='frequency',
                    ),
                ]),
            ], style={'width': '100%', 'display': 'none'}),
            dbc.Row([
                dbc.Col(
                    children=[
                        dbc.Button('Apply', id=f'aggregate-trends-alltime-apply', color="primary", className="mr-1", style={'display': 'none'}),
                    ]
                )
            ]),
            html.Br(),
            html.Br(),
            get_trends_table_frontend('aggregate-trends-alltime'),
            html.Button("Download CSV", id="aggregate-trends-all-download-btn"),
            dcc.Download(id="aggregate-trends-all-download-csv"),
        ]),
    ]
)

# Layout ------------------------------------------------------------------------
layout = html.Div(
    id='aggregate-trends-layout',
    className="p-3 bg-light rounded-3",
    children=[
        controls,
        html.Br(),
        html.Hr(),
        html.Br(),
        trends_period,
        html.Br(),
        html.Hr(),
        html.Br(),
        trends_compare,
        html.Br(),
        html.Hr(),
        html.Br(),
        trends_alltime,
    ]
)
