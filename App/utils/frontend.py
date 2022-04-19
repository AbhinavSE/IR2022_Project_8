from app import app
from dash.dependencies import Input, Output, State
from dash import html, dcc


def chartCSVDownloadButton(id_prefix):
    return html.Div([
        html.Button("Download CSV", id=f"{id_prefix}-download-btn"),
        dcc.Download(id=f"{id_prefix}-download-csv"),
    ])


def chartCSVDownloadButtonCallback(id_prefix, process_func=None, **kwargs):
    @app.callback(
        Output(f"{id_prefix}-download-csv", "data"),
        [Input(f"{id_prefix}-download-btn", "n_clicks"), State(f"{id_prefix}-data-table", "data")],
        prevent_initial_call=True,
    )
    def func(n_clicks, data):
        if process_func:
            chart_data = process_func(chart_data, kwargs)
        return dcc.send_data_frame(chart_data.to_csv, "news.csv", index=False)

    return func
