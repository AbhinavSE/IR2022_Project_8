from dash import html, dash_table as dt, dcc
import dash_bootstrap_components as dbc
from .news_callbacks import *

# Controls ---------------------------------------------------------------------
aggregate_news_controls = html.Div(
    id='aggregate-news-controls',
    children=[
        html.H3("Options"),
        html.Br(),
        dcc.Markdown('''
                ##### Custom Regex Syntax
                Operators:
                - and : &
                - or : |
                - not : ~
                - brackets : ()

                Regex string is surrounded in single quotes.
                Examples:
                - AWS or Amazon but no Azure or Microsoft in same news:
                    ```('aws' | 'amazon') & ~('azure' | 'microsoft')```
                    or
                    ```'aws|amazon' & ~'azure|microsoft'```
                - AWS with either google or azure news:
                    ```'aws|amazon' & (('google|gcp' & ~'azure|microsoft') | ('azure|microsoft' & ~'gcp|google'))```
            ''', style={'background-color': '#f7f7f7', 'padding': '10px'}),
        html.Br(),
        dbc.Row([
                dbc.Col(
                    [
                        dbc.InputGroup(
                            children=[
                                dbc.InputGroupText("Regex Include"),
                                dbc.Input(id='aggregate-news-regex-include', placeholder="Type your regex..."),
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
                                    id='aggregate-news-include-fields',
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
                        children=[dbc.InputGroupText("Regex Exclude"), dbc.Input(id='aggregate-news-regex-exclude', placeholder="Type your regex...")],
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
                                id='aggregate-news-exclude-fields',
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
                    dbc.Button('Apply', id='aggregate-news-apply-btn', color="primary", className="mr-1"),
                ]
            )
        ]),
    ]
)

# Table ------------------------------------------------------------------------
aggregate_news_table = html.Div(
    children=[
        html.H3("News"),
        dcc.Loading(
            id='aggregate-news-table-spinner',
            children=[
                dbc.Alert(id='aggregate-news-count', color='primary', children="No news found", style={'padding': '0.5rem', 'font-size': '0.7rem'}),
                dt.DataTable(
                    id='aggregate-news-tbl',
                    data=news(None).to_dict('records'),
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
                    page_current=0, page_size=20,
                    sort_action='native',
                    sort_mode='multi',
                    hidden_columns=['ID'],
                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                    persistence=True,
                    persistence_type='memory',
                ),
                html.Button("Download CSV", id="aggregate-news-download-btn"),
                dcc.Download(id="aggregate-news-download-csv"),
            ],
        ),
    ],
)

# Layout ------------------------------------------------------------------------
layout = html.Div(
    className="p-3 bg-light rounded-3",
    children=[
        html.Hr(),
        aggregate_news_controls,
        html.Hr(),
        aggregate_news_table,
    ]
)
