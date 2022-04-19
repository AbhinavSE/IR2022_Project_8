from datetime import datetime, date, timedelta
from dash import dcc
from dash.dependencies import Input, Output, State
from app import app
from pages.aggregate.data import get_tags
from pages.aggregate.sections.trends.trends_helper import *
from pages.aggregate.sidebar.sidebar_helper import SIDEBAR_INPUTS, get_sidebar_results
from pages.aggregate.utils.filters import get_applicable_news_ids

# Globals
NUM_COMPARISONS = 4


@app.callback(
    [Output('aggregate-trends-period-tbl-table', 'data'), Output('aggregate-trends-period-tbl-table', 'columns')],
    [
        *SIDEBAR_INPUTS,
        Input('aggregate-trends-tag-type', 'value'), Input('aggregate-trends-period-tbl-apply', 'n_clicks'),
        State('aggregate-trends-period-tbl-metric', 'value')
    ]
)
def get_trends_period_table(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, apply, metric):
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

        data = get_trends_table(data, tags, tag_type, metric)
    else:
        data = []
    cols = [] if len(data) == 0 else [{"name": i, "id": i, 'presentation': 'markdown'} for i in data[0].keys()]
    return data, cols


@app.callback(
    Output('aggregate-trends-period-timeseries-graph', 'figure'),
    [
        *SIDEBAR_INPUTS,
        Input('aggregate-trends-tag-type', 'value'), Input('aggregate-trends-period-timeseries-apply', 'n_clicks'),
        State('aggregate-trends-period-timeseries-metric', 'value'), State('aggregate-trends-period-timeseries-period', 'value')
    ]
)
def get_trends_period_timeseries(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, apply, metric, period):
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
        fig = get_trends_timeseries_graph(data, tags, tag_type, metric, period)
    else:
        fig = {}
    return fig


@app.callback(
    [Output("aggregate-trends-period-timeseries-modal", "is_open"), Output('aggregate-trends-period-timeseries-modal-header', 'children'),
     Output('aggregate-trends-period-timeseries-modal-table', 'data')],
    [
        *SIDEBAR_INPUTS,
        State('aggregate-trends-tag-type', 'value'), State('aggregate-trends-period-timeseries-period', 'value'), Input('aggregate-trends-period-timeseries-graph', 'clickData'),
        State('aggregate-trends-period-timeseries-graph', 'figure'), State("aggregate-trends-period-timeseries-modal", "is_open"),
    ],
)
def get_trends_timeseries_modal(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, period, clickData, fig, is_open):
    data = get_sidebar_results(db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url)
    if clickData is not None and not is_open:
        curve_number = clickData['points'][0]['curveNumber']
        x_value = clickData['points'][0]['x']
        trace_name = fig['data'][curve_number]['name']
        data = get_trends_timeseries_modal_data(data, trace_name, x_value, tag_type, period)
        return True, f"{trace_name} on {x_value if period !='month' else x_value[x_value.rfind('-')]}", data
    return is_open, '', []


@app.callback(
    [Output('aggregate-trends-alltime-table', 'data'), Output('aggregate-trends-alltime-table', 'columns')],
    [
        *SIDEBAR_INPUTS,
        Input('aggregate-trends-tag-type', 'value'), Input('aggregate-trends-alltime-apply', 'n_clicks'),
        State('aggregate-trends-alltime-metric', 'value')
    ]
)
def get_trends_overall(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, tag_type, apply, metric):
    data = get_sidebar_results(db_path, '2021/01/01', datetime.today().strftime('%Y/%m/%d'), markets, companies, products, keywords, operator, sources, external_url)
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
        data = get_trends_table(data, tags, tag_type, metric)
    else:
        data = []
    cols = [] if len(data) == 0 else [{"name": i, "id": i, 'presentation': 'markdown'} for i in data[0].keys()]
    return data, cols


@app.callback(
    Output("aggregate-trends-period-download-csv", "data"),
    [Input("aggregate-trends-period-download-btn", "n_clicks"), State("aggregate-trends-period-tbl-table", "data")],
    prevent_initial_call=True,
)
def download_period_trends(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, "trends.csv", index=False)


@app.callback(
    Output("aggregate-trends-all-download-csv", "data"),
    [Input("aggregate-trends-all-download-btn", "n_clicks"), State("aggregate-trends-alltime-table", "data")],
    prevent_initial_call=True,
)
def download_all_trends(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, "trends.csv", index=False)


@app.callback(
    [Output(f"aggregate-trends-compare-1-table", "data"), Output(f"aggregate-trends-compare-1-table", "columns")],
    [
        *SIDEBAR_INPUTS,
        Input('aggregate-trends-tag-type', 'value'), State(f"aggregate-trends-compare-k", "value"),
        Input(f"aggregate-trends-compare-apply", 'n_clicks'),
        Input(f"aggregate-trends-compare-1-start-date", "value"), Input(f"aggregate-trends-compare-1-end-date", "value"),
    ]
)
def get_trends_compare_table1(update, db_path, start_date, end_date, markets, companies, products, keywords, operator,
                              sources, external_url, tag_type, topk, apply, start_date_i, end_date_i):
    data = get_sidebar_results(db_path, start_date_i, end_date_i, markets, companies, products, keywords, operator, sources, external_url)
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
        data = get_trends_table(data, tags, tag_type, metric='Frequency')
        data = data[:topk]
    else:
        data = []
    cols = [] if len(data) == 0 else [{"name": i, "id": i, 'presentation': 'markdown'} for i in data[0].keys()]
    return data, cols


@app.callback(
    Output(f"aggregate-trends-compare-1-download", "data"),
    [Input(f"aggregate-trends-compare-1-download-btn", "n_clicks"), State(f"aggregate-trends-compare-1-table", "data")],
    prevent_initial_call=True,
)
def download_compare_trends(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, f"trends.csv", index=False)


@app.callback(
    [Output(f"aggregate-trends-compare-2-table", "data"), Output(f"aggregate-trends-compare-2-table", "columns")],
    [
        *SIDEBAR_INPUTS,
        Input('aggregate-trends-tag-type', 'value'), State(f"aggregate-trends-compare-k", "value"),
        Input(f"aggregate-trends-compare-apply", 'n_clicks'),
        Input(f"aggregate-trends-compare-2-start-date", "value"), Input(f"aggregate-trends-compare-2-end-date", "value"),
        Input(f"aggregate-trends-compare-1-table", "data")
    ]
)
def get_trends_compare_table2(update, db_path, start_date, end_date, markets, companies, products, keywords, operator,
                              sources, external_url, tag_type, topk, apply, start_date_i, end_date_i, data1):
    def add_rank_change_info(data: list, data1: list):
        init_tags = [t[tag_type] for t in data1]
        new_tags = [t[tag_type] for t in data]
        for row in data:
            # tag (rank change)
            tag = row[tag_type]
            if tag in init_tags:
                change = init_tags.index(tag) - new_tags.index(tag)
                if change != 0:
                    sign = '+' if change > 0 else '-'
                    row[tag_type] += f' ({sign}{abs(change)})'
                    row['rank_change'] = change
            else:
                row[tag_type] += ' (new)'
                row['rank_change'] = 1

        return data

    data = get_sidebar_results(db_path, start_date_i, end_date_i, markets, companies, products, keywords, operator, sources, external_url)
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
        data = get_trends_table(data, tags, tag_type, metric='Frequency')
        data = data[:topk]
        data = add_rank_change_info(data, data1)
    else:
        data = []
    cols = [] if len(data) == 0 else [{"name": i, "id": i, 'presentation': 'markdown'} for i in data[0].keys()]
    return data, cols


@app.callback(
    Output(f"aggregate-trends-compare-2-table", "style_data_conditional"),
    [Input(f"aggregate-trends-compare-2-table", "data"), Input(f"aggregate-trends-tag-type", "value")],
)
def set_trends_table_color(data, tag_type):
    if len(data) == 0:
        return []
    else:
        return [
            # if rank_change is positive then set First column to green, if neg then red, light blue if selected
            {
                'if': {'state': 'selected'},
                "backgroundColor": "inherit !important",
            },
            {
                'if': {'column_id': tag_type, 'filter_query': '{rank_change} > 0'},
                'background_color': '#d6f5d6',
            },
            {
                'if': {'column_id': tag_type, 'filter_query': '{rank_change} < 0'},
                'background_color': '#f5d6d6',
            },
        ]


@app.callback(
    Output(f"aggregate-trends-compare-2-download", "data"),
    [Input(f"aggregate-trends-compare-2-download-btn", "n_clicks"), State(f"aggregate-trends-compare-2-table", "data")],
    prevent_initial_call=True,
)
def download_compare_trends(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, "trends.csv", index=False)
