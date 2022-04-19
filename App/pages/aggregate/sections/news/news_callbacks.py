from app import app
from dash import dcc
from dash.dependencies import Input, Output, State
from utils.functions import get_tags_badges
from pages.aggregate.data import news
from pages.aggregate.sections.news.news_helper import prepare_for_download
from pages.aggregate.sidebar.sidebar_helper import get_sidebar_results
from pages.aggregate.utils.filters import get_applicable_news_ids
from copy import deepcopy
import dash_bootstrap_components as dbc


@app.callback(
    [Output('aggregate-news-tbl', 'data'), Output('aggregate-news-tbl', 'columns')],
    [
        # Sidebar Inputs
        Input('aggregate-sidebar-result', 'children'), State('aggregate-db-select', 'value'),
        State('aggregate-date-range', 'start_date'), State('aggregate-date-range', 'end_date'),
        State('aggregate-markets-dropdown', 'value'), State('aggregate-companies-dropdown', 'value'),
        State('aggregate-products-dropdown', 'value'), State('aggregate-keywords-dropdown', 'value'),
        State('aggregate-tags-operator', 'value'), State('aggregate-sources-switch', 'value'),
        State('aggregate-url-switch', 'value'),
        # Section Inputs
        State('aggregate-news-regex-include', 'value'), State('aggregate-news-regex-exclude', 'value'),
        State('aggregate-news-include-fields', 'value'), State('aggregate-news-exclude-fields', 'value'),
        Input('aggregate-news-apply-btn', 'n_clicks')
    ]
)
def search_news(update, db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url, inc_regex, exc_regex, inc_field, exc_field, apply):
    print('Getting News table')
    data = get_sidebar_results(db_path, start_date, end_date, markets, companies, products, keywords, operator, sources, external_url)
    inc_regex = inc_regex if inc_regex else ''
    exc_regex = exc_regex if exc_regex else ''
    filtered_ids = get_applicable_news_ids(
        data,
        inc_regex={'regex': inc_regex, 'fields': inc_field},
        exc_regex={'regex': exc_regex, 'fields': exc_field},
    )
    filtered_news = [deepcopy(t) for t in data if t['ID'] in filtered_ids][:600]
    for news in filtered_news:
        news['tags'] = get_tags_badges(news['tags'])

    cols = [{"name": c, "id": c, 'presentation': 'markdown'} for c in filtered_news[0].keys()
            if c in ['Date', 'News Text', 'Source URL', 'External URL', 'tags']] if len(filtered_news) > 0 else []

    return filtered_news, cols


@app.callback(
    Output('aggregate-news-count', 'children'),
    [Input('aggregate-news-tbl', 'data')]
)
def update_news_count(data):
    return f"{len(data)} news found"


@app.callback(
    Output("aggregate-news-download-csv", "data"),
    [Input("aggregate-news-download-btn", "n_clicks"), State("aggregate-news-tbl", "data")],
    prevent_initial_call=True,
)
def func(n_clicks, data):
    data = prepare_for_download(data)
    return dcc.send_data_frame(data.to_csv, "news.csv", index=False)
