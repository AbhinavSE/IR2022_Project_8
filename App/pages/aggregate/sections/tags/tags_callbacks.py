from copy import deepcopy
from dash.dependencies import Input, Output, State
from dash import html, dcc
import pandas as pd
from app import app
import dash_bootstrap_components as dbc
from pages.aggregate.data import get_tags, news
from pages.aggregate.sections.tags.tags_helper import *
from pages.aggregate.sidebar.sidebar_helper import get_sidebar_results
from utils.functions import get_tags_badges


@app.callback(
    [Output('aggregate-tags-data-table', 'data'), Output('aggregate-tags-data-table', 'columns')],
    [
        # Sidebar Inputs
        Input('aggregate-sidebar-result', 'children'), State('aggregate-db-select', 'value'),
        State('aggregate-date-range', 'start_date'), State('aggregate-date-range', 'end_date'),
        State('aggregate-markets-dropdown', 'value'), State('aggregate-companies-dropdown', 'value'),
        State('aggregate-products-dropdown', 'value'), State('aggregate-keywords-dropdown', 'value'),
        State('aggregate-tags-operator', 'value'), State('aggregate-sources-switch', 'value'),
        State('aggregate-url-switch', 'value'),

        # Section Inputs
        Input('aggregate-tag-type', 'value'), Input('aggregate-tags-data-apply', 'n_clicks'),
        State('aggregate-tags-data-k-tags', 'value'), State('aggregate-tags-data-metric', 'value'),
        State('aggregate-tags-regex-include', 'value'), State('aggregate-tags-regex-exclude', 'value'),
        State('aggregate-tags-include-fields', 'value'), State('aggregate-tags-exclude-fields', 'value'), ]
)
def get_tags_data_table(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources,
                        external_url, tag_type, apply, k_tags, metric, inc_regex, exc_regex, inc_field, exc_field):
    data = get_sidebar_results(db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url)
    cols = []
    if db_path != 'None':
        tags = None
        if tag_type == 'keywords':
            tags = pd.DataFrame(get_tags(db_path)['keyword_tags'])
        else:
            tags = pd.DataFrame(get_tags(db_path)['product_tags'])
            if tag_type == 'products':
                if companies:
                    tags = tags[tags['companies'].isin(companies)]
                if markets:
                    tags = tags[tags['markets'].isin(markets)]
                if products:
                    tags = tags[tags['products'].isin(products)]

        inc_regex = inc_regex if inc_regex else ''
        exc_regex = exc_regex if exc_regex else ''
        filtered_ids = get_applicable_news_ids(
            data,
            inc_regex={'regex': inc_regex, 'fields': inc_field},
            exc_regex={'regex': exc_regex, 'fields': exc_field},
        )
        data = [deepcopy(t) for t in data if t['ID'] in filtered_ids]
        data = get_data_table(data, tags, tag_type, k_tags, metric)[:400]

        for news in data:
            news['tags'] = get_tags_badges(news['tags'])

        cols = [{"name": c, "id": c, 'presentation': 'markdown'} for c in data[0].keys()
                if c in ['Date', 'News Text', 'Source URL', 'External URL', 'tags']] if len(data) > 0 else []
    else:
        data = []

    return data, cols


@app.callback(
    Output('aggregate-tags-timeseries-graph', 'figure'),
    [
        # Sidebar Inputs
        Input('aggregate-sidebar-result', 'children'), State('aggregate-db-select', 'value'),
        State('aggregate-date-range', 'start_date'), State('aggregate-date-range', 'end_date'),
        State('aggregate-markets-dropdown', 'value'), State('aggregate-companies-dropdown', 'value'),
        State('aggregate-products-dropdown', 'value'), State('aggregate-keywords-dropdown', 'value'),
        State('aggregate-tags-operator', 'value'), State('aggregate-sources-switch', 'value'),
        State('aggregate-url-switch', 'value'),

        # Section Inputs
        Input('aggregate-tag-type', 'value'), Input('aggregate-tags-timeseries-apply', 'n_clicks'),
        State('aggregate-tags-timeseries-k-tags', 'value'),
        State('aggregate-tags-timeseries-metric', 'value'), State('aggregate-tags-timeseries-period', 'value')]
)
def get_tags_timeseries(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, apply, k_tags, metric, period):
    data = get_sidebar_results(db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url)
    if db_path != 'None':
        tags = None
        if tag_type == 'keywords':
            tags = pd.DataFrame(get_tags(db_path)['keyword_tags'])
        else:
            tags = pd.DataFrame(get_tags(db_path)['product_tags'])
            if tag_type == 'products':
                if companies:
                    tags = tags[tags['companies'].isin(companies)]
                if markets:
                    tags = tags[tags['markets'].isin(markets)]
                if products:
                    tags = tags[tags['products'].isin(products)]
        fig = get_tags_timeseries_graph(data, tags, tag_type, k_tags, metric, period)
    else:
        fig = {}
    return fig


@app.callback(
    [Output("aggregate-tags-timeseries-modal", "is_open"), Output('aggregate-tags-timeseries-modal-header', 'children'),
     Output('aggregate-tags-timeseries-modal-table', 'data')],
    [
        # Sidebar Inputs
        State('aggregate-sidebar-result', 'children'), State('aggregate-db-select', 'value'),
        State('aggregate-date-range', 'start_date'), State('aggregate-date-range', 'end_date'),
        State('aggregate-markets-dropdown', 'value'), State('aggregate-companies-dropdown', 'value'),
        State('aggregate-products-dropdown', 'value'), State('aggregate-keywords-dropdown', 'value'),
        State('aggregate-tags-operator', 'value'), State('aggregate-sources-switch', 'value'),
        State('aggregate-url-switch', 'value'),

        # Section Inputs
        State('aggregate-tag-type', 'value'), State('aggregate-tags-timeseries-k-tags', 'value'),
        State('aggregate-tags-timeseries-metric', 'value'),
        State('aggregate-tags-timeseries-period', 'value'), Input('aggregate-tags-timeseries-graph', 'clickData'),
        State('aggregate-tags-timeseries-graph', 'figure'), State("aggregate-tags-timeseries-modal", "is_open"),
    ],
)
def get_tags_timeseries_modal(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, k_tags, metric, period, clickData, fig, is_open):
    data = get_sidebar_results(db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url)
    if clickData is not None and not is_open:
        curve_number = clickData['points'][0]['curveNumber']
        x_value = clickData['points'][0]['x']
        trace_name = fig['data'][curve_number]['name']
        data = get_tags_timeseries_modal_data(data, trace_name, x_value, tag_type, period)
        return True, f"{trace_name} on {x_value if period !='month' else x_value[x_value.rfind('-')]}", data
    return is_open, '', []


@app.callback(
    Output("aggregate-tags-download-csv", "data"),
    [Input("aggregate-tags-download-btn", "n_clicks"), State("aggregate-tags-data-table", "data")],
    prevent_initial_call=True,
)
def func(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, "news.csv", index=False)
