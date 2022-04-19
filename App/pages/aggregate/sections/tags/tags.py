from dash import html, dash_table as dt, dcc
import dash_bootstrap_components as dbc
from .tags_callbacks import *

# Controls ---------------------------------------------------------------------
controls = html.Div(
    id='aggregate-tags-controls',
    children=[
        html.H3("Options"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Tag Type"),
                dbc.Select(
                    id='aggregate-tag-type',
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


# Table ------------------------------------------------------------------------
tags_data_table = html.Div(
    id='aggregate-tags-data-table',
    children=[
        html.H3("Tags Data Table"),
        dcc.Loading([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Top k Tags"),
                    dbc.Input(id='aggregate-tags-data-k-tags', type="number", min=0, step=1, value=500),
                ]),
                dbc.Col([
                    dbc.Label("Metric"),
                    dbc.Select(
                        id='aggregate-tags-data-metric',
                        options=[
                            {'label': 'Frequency', 'value': 'frequency'},
                        ],
                        value='frequency',
                    ),
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    [
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("Regex Include"),
                                dbc.Input(id='aggregate-tags-regex-include', placeholder="Type your regex..."),
                            ],
                            size="sm",
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("In"),
                                dcc.Dropdown(
                                    id='aggregate-tags-include-fields',
                                    options=[
                                        {'label': 'News Text', 'value': 'News Text'},
                                        {'label': 'Source URL', 'value': 'Source URL'},
                                        {'label': 'External URL', 'value': 'External URL'},
                                    ],
                                    value=['News Text'],
                                    placeholder="Select fields...",
                                    multi=True,
                                    style={'width': '90%'}
                                ),
                            ],
                            size="sm",
                        ),
                    ],
                ),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    [
                        dbc.InputGroup(
                            children=[dbc.InputGroupText("Regex Exclude"), dbc.Input(id='aggregate-tags-regex-exclude', placeholder="Type your regex...")],
                            size="sm",
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("In"),
                                dcc.Dropdown(
                                    id='aggregate-tags-exclude-fields',
                                    options=[
                                        {'label': 'News Text', 'value': 'News Text'},
                                        {'label': 'Source URL', 'value': 'Source URL'},
                                        {'label': 'External URL', 'value': 'External URL'},
                                    ],
                                    value=['News Text'],
                                    placeholder="Select fields...",
                                    multi=True,
                                    style={'width': '90%'}
                                ),
                            ],
                            size="sm",
                        ),
                    ]
                ),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    children=[
                        dbc.Button('Apply', id=f'aggregate-tags-data-apply', color="primary", className="mr-1"),
                    ]
                )
            ]),
            dt.DataTable(
                id='aggregate-tags-data-table',
                data=[],
                columns=[],
                # Style
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell={
                    'font-family': 'Helvetica',
                    'font-size': '0.8rem',
                    'text-align': 'center',
                    'padding': '0.3rem',
                },
                # Functions
                page_current=0, page_size=10,
                sort_action='native',
                sort_mode='multi',
                hidden_columns=['ID'],
                css=[{"selector": ".show-hide", "rule": "display: none"}],
                persistence=True,
                persistence_type='memory',
                style_table={'overflowX': 'scroll'}
            ),
            html.Button("Download CSV", id="aggregate-tags-download-btn"),
            dcc.Download(id="aggregate-tags-download-csv"),
        ]),
    ],
)

tags_timeseries = get_tags_graphs_frontend(title='Tags Timeseries', id_prefix='aggregate-tags-timeseries')


tags_graphs = html.Div(
    id='aggregate-tags-graphs',
    children=[
        html.H3('Tags Graphs'),
        html.Br(),
        tags_timeseries,
    ]
)

# Layout ------------------------------------------------------------------------
layout = html.Div(
    id='aggregate-tags-layout',
    className="p-3 bg-light rounded-3",
    children=[
        html.Hr(),
        controls,
        html.Br(),
        html.Hr(),
        html.Br(),
        tags_data_table,
        html.Br(),
        html.Hr(),
        html.Br(),
        tags_graphs
    ]
)
