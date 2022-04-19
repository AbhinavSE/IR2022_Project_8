import collections
from collections import Counter
import re
import pandas as pd
from pages.aggregate.data import news
from pages.aggregate.utils.filters import get_applicable_news_ids
from plotly import graph_objects
import plotly.express as px
from dash import html, dash_table as dt, dcc
import dash_bootstrap_components as dbc
from utils.caching import cache, TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def get_topk_tags(tweets_list, in_tags, tag_type, k_tags, metric):
    tags = collections.defaultdict(lambda: 0)
    for tweet in tweets_list:
        if tag_type in tweet['tags']['primary']:
            for k in tweet['tags']['primary'][tag_type]:
                if k in in_tags:
                    tags[k] += 1 if metric == 'frequency' else 0
    topk_tags = [t[0] for t in Counter(tags).most_common(k_tags)]
    return topk_tags


def get_data_table(tweets_list, in_tags, tag_type, k_tags, metric):
    '''An agrid table to show all the tweets based on the chosen parameters'''
    in_tags = in_tags[tag_type].unique().tolist()
    topk_tags = get_topk_tags(tweets_list, in_tags, tag_type, k_tags, metric)

    show_tweets = []
    for tweet in tweets_list:
        if tag_type in tweet['tags']['primary']:
            for k in tweet['tags']['primary'][tag_type]:
                if k in topk_tags:
                    show_tweets.append({
                        'ID': tweet['ID'],
                        'Date': tweet['Date'],
                        'News Text': tweet['News Text'],
                        'Source URL': tweet['Source URL'],
                        'External URL': tweet['External URL'],
                        'Source': tweet['Source'],
                        'tags': tweet['tags']
                    })
                    break

    if len(show_tweets) > 0:
        show_tweets = pd.DataFrame(show_tweets)
        show_tweets = show_tweets.sort_values(by='Date', ascending=False).reset_index(drop=True).to_dict('records')
        return show_tweets
    return []


def get_tags_timeseries_graph(tweets_list, tags, tag_type, k_tags, metric, period):
    ''' Plot the tags timeseries '''

    in_tags = tags[tag_type].unique().tolist()
    topk_tags = get_topk_tags(tweets_list, in_tags, tag_type, k_tags, metric)

    tweets = []
    tags_in_graph = set()
    for tweet in tweets_list:
        if tag_type in tweet['tags']['primary']:
            t = {'Date': tweet['Date']}
            for tk in list(tweet['tags']['primary'][tag_type]):
                if tk in in_tags:
                    t[tk] = 1 if metric == 'frequency' else 0
                else:
                    t[tk] = 0
                tags_in_graph.add(tk)
            tweets.append(t)
    tweets = pd.DataFrame(tweets)
    tweets.fillna(0, inplace=True)
    period = 'D' if period == 'daily' else ('W' if period == 'weekly' else 'M')

    if len(tweets) > 0:
        tweets['Date'] = pd.to_datetime(tweets['Date']).dt.to_period(period).dt.to_timestamp()
        tweets = tweets.groupby('Date').sum()[topk_tags]
        # sort columnns based on col sum
        tweets = tweets[tweets.sum().sort_values(ascending=False).index]
        fig = graph_objects.Figure()
        for col in tweets.columns:
            # hoverinnfo shows tag name annd tweet count
            fig.add_trace(graph_objects.Scatter(x=tweets.index, y=tweets[col], name=col, mode='lines+markers', hoverinfo='name+y'))

        fig.update_layout(
            width=1100, height=400,
            title='Tags TimeSeries Graph',
            legend_title=f'Top {tag_type}',
            xaxis=dict(
                title='Date Time', showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204,204,204)', linewidth=2, ticks='outside',
                tickfont=dict(family='Arial', size=10, color='rgb(82,82,82)')
            ),
            yaxis=dict(
                title=metric, showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204,204,204)', linewidth=2, ticks='outside',
                tickfont=dict(family='Arial', size=10, color='rgb(82,82,82)',)
            ),
        )
        fig.update_layout(xaxis_tickangle=-45, hoverlabel=dict(font_size=10, namelength=-1), legend=dict(font=dict(size=10)))
        if period == 'M':
            fig.update_xaxes(dtick="M1", tickformat='%b %Y')
        return fig
    return {}


def get_tags_timeseries_modal_data(data, trace_name, x_value, tag_type, period):
    ''' Get the modal data for the tags timeseries graph'''
    period = 'D' if period == 'daily' else ('W' if period == 'weekly' else 'M')
    data = pd.DataFrame(data)
    data['Date'] = pd.to_datetime(data['Date']).dt.to_period(period).dt.to_timestamp()
    data = data[data['Date'] == x_value]
    modal_data = []

    def add_applicable_tweets(tweet):
        date = tweet['Date'].strftime('%Y-%m-%d')
        if date == x_value and \
                tag_type in tweet['tags']['primary'] and trace_name in tweet['tags']['primary'][tag_type]:

            modal_data.append({
                'Date': date,
                'News Text': tweet['News Text'],
                'Source URL': tweet['Source URL'],
                'External URL': tweet['External URL']
            })
    data.apply(add_applicable_tweets, axis=1)
    return modal_data


def get_tags_graphs_frontend(title, id_prefix, period=True):
    return html.Div(
        id=id_prefix,
        children=[
            html.H5(title),
            dcc.Loading([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Top k Tags"),
                        dbc.Input(id=f'{id_prefix}-k-tags', type="number", min=0, step=1, value=500, persistence=True, persistence_type='memory'),
                    ]),
                    dbc.Col([
                        dbc.Label("Metric"),
                        dbc.Select(
                            id=f'{id_prefix}-metric',
                            options=[
                                {'label': 'Frequency', 'value': 'frequency'},
                            ],
                            value='frequency',
                            persistence=True,
                            persistence_type='memory',
                        ),
                    ]),
                    dbc.Col([
                        dbc.Label("Period"),
                        dbc.Select(
                            id=f'{id_prefix}-period',
                            options=[
                                {'label': 'Monthly', 'value': 'monthly'},
                                {'label': 'Weekly', 'value': 'weekly'},
                                {'label': 'Daily', 'value': 'daily'},
                            ],
                            value='daily',
                            persistence=True,
                            persistence_type='memory',
                        ),
                    ], style={'display': 'none'} if not period else {}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            children=[
                                dbc.Button('Apply', id=f'{id_prefix}-apply', color="primary", className="mr-1"),
                            ]
                        )
                    ]),
                    dcc.Graph(id=f'{id_prefix}-graph', style={'zoom': '133.33%'}),
                    dbc.Modal(
                        id=f'{id_prefix}-modal',
                        size="lg",
                        children=[
                            dbc.ModalHeader(id=f'{id_prefix}-modal-header'),
                            dbc.ModalBody(
                                dt.DataTable(
                                    id=f'{id_prefix}-modal-table',
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
                ])
            ]),
        ])


def prepare_for_download(data):
    data = pd.DataFrame(data)
    if data is not None:
        bracket_regex = re.compile(r'\((.*?)\)')
        data['Source URL'] = data['Source URL'].apply(
            lambda x: f'=HYPERLINK("{bracket_regex.search(x).group(1)}")' if bracket_regex.search(x) else x
        )
        data['External URL'] = data['External URL'].apply(
            lambda x: f'=HYPERLINK("{bracket_regex.search(x).group(1)}")' if bracket_regex.search(x) else x
        )
        data = data[['ID', 'Date', 'News Text', 'Source URL', 'External URL', 'Source', 'tags']]
    return data
