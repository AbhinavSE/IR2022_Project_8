
from datetime import date
import re
import pandas as pd
from utils.functions import is_twitter_url, isna
from utils.nlp import checkRegexp


def is_date_applicable(news, start_date, end_date):
    return True if (start_date <= news['Date'] <= end_date) else False


def is_tag_applicable(news, in_tags):
    if len(news['tags']['primary']) == 0:
        return 0

    match = 0
    inc_type = 'primary'
    if 'markets' in in_tags:
        for market in in_tags['markets']:
            if 'markets' in news['tags'][inc_type] and market in news['tags'][inc_type]['markets']:
                if match == 0:
                    match = 1
                if market in news['tags']['primary']['markets']:
                    match += 1
            elif in_tags['op'] == 'AND':
                return 0

    if 'companies' in in_tags:
        for company in in_tags['companies']:
            if 'companies' in news['tags'][inc_type] and company in news['tags'][inc_type]['companies']:
                if match == 0:
                    match = 1
                if company in news['tags']['primary']['companies']:
                    match += 1
            elif in_tags['op'] == 'AND':
                return 0

    if 'products' in in_tags:
        for product in in_tags['products']:
            if 'products' in news['tags'][inc_type] and product in news['tags'][inc_type]['products']:
                if match == 0:
                    match = 1
                if product in news['tags']['primary']['products']:
                    match += 3
            elif in_tags['op'] == 'AND':
                return 0

    if 'keywords' in in_tags:
        for keyword in in_tags['keywords']:
            if 'keywords' in news['tags'][inc_type] and keyword in news['tags'][inc_type]['keywords']:
                if match == 0:
                    match = 1
                if keyword in news['tags']['primary']['keywords']:
                    match += 1
            elif in_tags['op'] == 'AND':
                return 0

    if 'search' in in_tags:
        for search in in_tags['search']:
            if 'search' in news['tags'][inc_type] and search in news['tags'][inc_type]['search']:
                if match == 0:
                    match = 1
                if search in news['tags']['primary']['search']:
                    match += 1
            elif in_tags['op'] == 'AND':
                return 0
    return match


def is_regex_applicable(news, regex_include={}, regex_exclude={}, regex_ignorecase=True):
    if (len(regex_include) != 2 or len(regex_exclude) != 2):
        return True
    if regex_exclude['regex'] != '':
        for col in regex_exclude['fields']:
            if checkRegexp(regex_exclude['regex'], str(news[col])):
                return False
    if regex_include['regex'] != '':
        for col in regex_include['fields']:
            if checkRegexp(regex_include['regex'], str(news[col])):
                return True
        return False
    return True


def is_source_applicable(news, sources):
    if len(sources) == 0:
        return True
    return news['Source'] in sources


def has_external_url(news, url_only=[]):
    if len(url_only) == 2 or len(url_only) == 0 or 'twitter' not in news['Source']:
        return True
    for url in news['External URL']:
        if not is_twitter_url(url):
            if 'url' in url_only:
                return True
            else:
                return False
    return True if 'non_url' in url_only else False


def is_news_applicable(news, start_date, end_date, in_tags, inc_regex, exc_regex, sources, url_only):
    if all(len(v) == 0 if t != 'op' else True for t, v in in_tags.items()):
        news['match'] = 1
    else:
        news['match'] = is_tag_applicable(news, in_tags)
    is_app = news['match'] and \
        has_external_url(news, url_only) and \
        is_date_applicable(news, start_date, end_date) and \
        is_regex_applicable(news, inc_regex, exc_regex) and \
        is_source_applicable(news, sources)
    return is_app


def get_applicable_news_ids(news_list, start_date=date(1970, 1, 1).strftime('%Y/%m/%d'), end_date=date.today().strftime('%Y/%m/%d'),
                            in_tags={}, inc_regex={}, exc_regex={}, sources=[], external_url=[]):
    news_ids = set()
    for news in news_list:
        if is_news_applicable(news, start_date, end_date, in_tags, inc_regex, exc_regex, sources, external_url):
            news_ids.add(news['ID'])

    return news_ids
