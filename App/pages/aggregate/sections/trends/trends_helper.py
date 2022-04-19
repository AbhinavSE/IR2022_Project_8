import collections
from datetime import date, timedelta, datetime
from time import time
import pandas as pd
from dash import html, dcc
import dash.dash_table as dt
import dash_bootstrap_components as dbc
from utils.caching import TIMEOUT, cache
from plotly import graph_objects


@cache.memoize(timeout=TIMEOUT)
def get_trends_table(tweets_list, tags, tag_type, metric):
    """ Get the trends table """
    tags_dict = collections.defaultdict(lambda: {tag_type: '', 'Frequency': 0, 'Score': 0})
    unique_p = set(tags['products'].unique()) if tag_type == 'products' else set()
    tags = {pt['products']: pt for pt in tags.to_dict('records')} if tag_type == 'products' else {}
    for t in tweets_list:
        if tag_type in t['tags']['primary']:
            for tag in t['tags']['primary'][tag_type]:
                if tag_type != 'products' or tag in unique_p:
                    tags_dict[tag][tag_type] = tag
                    tags_dict[tag][f'Frequency'] += 1
                    if tag_type == 'products':
                        tags_dict[tag]['Company'] = tags[tag]['companies']
                        tags_dict[tag]['Market'] = tags[tag]['markets']

    tags_df = pd.DataFrame(tags_dict.values())
    tags_df.fillna(0, inplace=True)
    if len(tags_df) > 0:
        if tag_type == 'products':
            tags_df = tags_df.reindex([tag_type, 'Frequency', 'Company', 'Market'], axis=1)
        else:
            tags_df = tags_df.reindex([tag_type, 'Frequency'], axis=1)
        tags_df.sort_values(by=[metric.title()], ascending=False, inplace=True)
        return tags_df.to_dict(orient='records')
    return []


def get_trends_timeseries_graph(tweets_list, tags, tag_type, metric, period):
    in_tags = set(tags[tag_type].unique())
    tweets = []
    for tweet in tweets_list:
        if tag_type in tweet['tags']['primary']:
            t = {'Date': tweet['Date']}
            t = {**t, **{tag: 0 for tag in in_tags}}
            for tk in list(tweet['tags']['primary'][tag_type]):
                if tk in in_tags:
                    t[tk] = 1 if metric == 'frequency' else 0
            tweets.append(t)
    tweets = pd.DataFrame(tweets)
    tweets.fillna(0, inplace=True)
    period = 'D' if period == 'daily' else ('W' if period == 'weekly' else 'M')

    if len(tweets) > 0:
        tweets['Date'] = pd.to_datetime(tweets['Date']).dt.to_period(period).dt.to_timestamp()
        tweets = tweets.groupby('Date').sum()[list(in_tags)]
        # sort columnns based on col sum
        tweets = tweets[tweets.sum().sort_values(ascending=False).index]
        fig = graph_objects.Figure()
        for col in tweets.columns:
            # hoverinfo shows tag name and tweet count
            fig.add_trace(graph_objects.Scatter(x=tweets.index, y=tweets[col], name=col, mode='lines+markers',
                                                hoverinfo='name+y'))

        fig.update_layout(
            width=1100, height=400,
            title='Tweets TimeSeries Graph',
            legend_title=f'Top {tag_type}',
            xaxis=dict(
                title='Date Time', showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204,204,204)',
                linewidth=2, ticks='outside',
                tickfont=dict(family='Arial', size=10, color='rgb(82,82,82)')
            ),
            yaxis=dict(
                title=metric, showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204,204,204)',
                linewidth=2, ticks='outside',
                tickfont=dict(family='Arial', size=10, color='rgb(82,82,82)')
            ),
        )
        fig.update_layout(xaxis_tickangle=-45, hoverlabel=dict(font_size=10, namelength=-1),
                          legend=dict(font=dict(size=10)))
        if period == 'M':
            fig.update_xaxes(dtick="M1", tickformat='%b %Y')
        return fig
    return {}


def get_trends_timeseries_modal_data(data, trace_name, x_value, tag_type, period):
    """ Get the modal data for the tags timeseries graph"""
    period = 'D' if period == 'daily' else ('W' if period == 'weekly' else 'M')
    data = pd.DataFrame(data)
    data['Date'] = pd.to_datetime(data['Date']).dt.to_period(period).dt.to_timestamp()
    data = data[data['Date'] == x_value]
    modal_data = []

    def add_applicable_news(news):
        date = news['Date'].strftime('%Y-%m-%d')
        if date == x_value and tag_type in news['tags']['primary'] and trace_name in news['tags']['primary'][tag_type]:
            modal_data.append({
                'Date': date,
                'News Text': news['News Text'],
                'Source URL': news['Source URL'],
                'External URL': news['External URL']
            })

    data.apply(add_applicable_news, axis=1)
    return modal_data


def prepare_for_download(data):
    data = pd.DataFrame(data)
    return data


def get_trends_table_frontend(id_prefix, data=None):
    if data is None:
        data = []
    return dcc.Loading([dt.DataTable(
        id=f'{id_prefix}-table',
        data=data,
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
        persistence=True,
        persistence_type='memory',
        style_table={'overflowX': 'scroll', 'width': '100%'},
    )])


def get_date_range_frontend(id_prefix, start_date=None, end_date=None):
    if start_date is None:
        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")
    return html.Div([
        dbc.Label("Date Range"),
        dcc.DatePickerRange(
            id=f"{id_prefix}-daterange",
            min_date_allowed='2021-01-01',
            max_date_allowed=date.today().strftime("%Y-%m-%d"),
            start_date=start_date,
            end_date=end_date,
            display_format="MMM Do, YY",
            style={'width': '100%'},
            persistence=True,
            persistence_type='memory',
        )
    ])


def get_n_trends_comparisons(num_comparisons):
    """Get num_comparisons number of date range control, top k control and tables for trends comparison with 2 tables
    per row """
    def get_ith_cell(i):
        return dbc.Col([
            html.Br(),
            html.H5(f'Trend {i+1}'),
            get_date_range_frontend(f'aggregate-trends-compare-{i}'),
            get_trends_table_frontend(f'aggregate-trends-compare-{i}'),
            html.Button("Download CSV", id=f'aggregate-trends-compare-{i}-download-btn'),
            dcc.Download(id=f'aggregate-trends-compare-{i}-download'),
        ])

    children = []
    for i in range(0, num_comparisons, 2):
        row = dbc.Row([get_ith_cell(i)])
        if i + 1 < num_comparisons:
            row.children += [get_ith_cell(i + 1)]
        children.append(row)
    return children
