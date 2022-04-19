import re
import pandas as pd


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
