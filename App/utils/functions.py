from dateutil import tz
import numpy as np
import pandas as pd
from utils.caching import cache, TIMEOUT
from utils.drive.drive_helper import get_json_from_drive


@cache.memoize(TIMEOUT)
def get_user_data():
    return get_json_from_drive('user_data.json')[0]


def change_timezone(dates):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    return [date.replace(tzinfo=from_zone).astimezone(to_zone) if not isna(date) else None for date in dates.tolist()]


def isna(var):
    return True if var is None or var is np.nan or pd.isna(var) or str(var) == 'None' or str(var) == 'NaN' or str(var) == 'nan' else False


def is_twitter_url(url):
    return 'https://twitter.com/' in url


def get_tags_badges(tags):
    tags_badges = []

    if 'companies' in tags['primary']:
        for tag in tags['primary']['companies']:
            tags_badges.append(f'[![Generic badge](https://img.shields.io/badge/{tag}-blue.svg)](https://shields.io/)')

    if 'products' in tags['primary']:
        for tag in tags['primary']['products']:
            tags_badges.append(f'[![Generic badge](https://img.shields.io/badge/{tag.replace(" ", "_")}-red.svg)](https://shields.io/)')

    if 'keywords' in tags['primary']:
        for tag in tags['primary']['keywords']:
            tags_badges.append(f'[![Generic badge](https://img.shields.io/badge/{tag.replace(" ", "_")}-green.svg)](https://shields.io/)')

    return ' '.join(tags_badges)
