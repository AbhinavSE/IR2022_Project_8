from utils.caching import cache, TIMEOUT
import pandas as pd
from utils.functions import change_timezone, isna
from utils.nlp import extract_domain
from utils.s3 import S3Helper


@cache.memoize(timeout=TIMEOUT)
def get_tags(db_path):
    s3 = S3Helper()
    if db_path is None or db_path == 'None':
        return None
    domain = 'cloud' if 'cloud' in db_path else 'Error'
    tags_dict = s3.read_json(f'data/other_data/{domain}/tags.json')
    if domain == 'cloud':
        tags_dict['product_tags'] = pd.DataFrame(tags_dict['product_tags'])
        tags_dict['keyword_tags'] = pd.DataFrame(tags_dict['keyword_tags'])
    return tags_dict


@cache.memoize(timeout=TIMEOUT)
def load_db(db_path):
    print('Cache not used')
    s3 = S3Helper()
    if db_path is None or db_path == 'None':
        return pd.DataFrame(columns=['ID', 'Date', 'News Text', 'Source URL', 'tags', 'Source', 'External URL'])
    elif 'cloud' in db_path:
        paths = ['cloud/twitter/csp3_tweets.csv', 'cloud/twitter/noncsp3_tweets.csv', 'cloud/google/csp3_news.csv', 'cloud/media/news.csv']
        df = pd.DataFrame(columns=['ID', 'Date', 'News Text', 'Source URL', 'tags', 'External URL'])
        for path in paths:
            print(path)
            if 'twitter' in path:
                df_path = s3.read_csv(f'data/databases/{path}')
                df_path[['ID', 'Created_At', 'Tweet_Text', 'Source_Url', 'tags', 'Urls']]
                df_path.rename(columns={'ID': 'ID', 'Created_At': 'Date', 'Tweet_Text': 'News Text', 'Source_Url': 'Source URL', 'tags': 'tags', 'Urls': 'External URL'}, inplace=True)
                df_path['Source'] = path.split('/')[1] + '_' + path.split('/')[-1]
                print(path.split('/')[1] + '_' + path.split('/')[-1])
                df = pd.concat([df, df_path], ignore_index=True)

            elif 'google' in path:
                df_path = s3.read_csv(f'data/databases/{path}')
                df_path[['id', 'publishedAt', 'title', 'description', 'url', 'tags']]
                df_path['News Text'] = '**' + df_path['title'] + ':**\n' + df_path['description']
                df_path.drop(columns=['title', 'description'], inplace=True)
                df_path.rename(columns={'id': 'ID', 'publishedAt': 'Date', 'url': 'Source URL', 'tags': 'tags'}, inplace=True)
                df_path['Source'] = path.split('/')[1] + '_' + path.split('/')[-1]
                print(path.split('/')[1] + '_' + path.split('/')[-1])

                df = pd.concat([df, df_path], ignore_index=True)
            elif 'media' in path:
                df_path = s3.read_csv(f'data/databases/{path}')
                df_path[['publish_date', 'title', 'description', 'url', 'tags']]
                df_path['ID'] = df_path.index + 1
                df_path['News Text'] = '**' + df_path['title'] + ':**\n' + df_path['description']
                df_path.drop(columns=['title', 'description'], inplace=True)
                df_path.rename(columns={'publish_date': 'Date', 'url': 'Source URL', 'tags': 'tags'}, inplace=True)
                df_path['Source'] = path.split('/')[1] + '_' + path.split('/')[-1]
                print(path.split('/')[1] + '_' + path.split('/')[-1])
                df = pd.concat([df, df_path], ignore_index=True)
            else:
                print('Invalid path')
    df = df.dropna(subset=['News Text', 'Date', 'Source URL'])
    df = df.fillna('')
    df['Date'] = pd.to_datetime(df['Date'], format=f'%Y-%m-%d %H:%M:%S', errors='ignore')
    df['Date'] = change_timezone(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')
    df['tags'] = df['tags'].apply(lambda x: eval(x) if not isna(x) and x != '' else {'primary': {}, 'secondary': {}})
    df['Source URL'] = df['Source URL'].apply(lambda x: eval('["' + x + '"]') if not isna(x) else [])
    df['Source URL'] = df['Source URL'].apply(lambda x: (f'[{extract_domain(x[0])}]({x[0]})') if len(x) > 0 else '')
    df['External URL'] = df['External URL'].apply(lambda x: eval(x) if not isna(x) and x != '' else [])
    df['External URL'] = df['External URL'].apply(lambda x: (f'[{extract_domain(x[0])}]({x[0]})') if len(x) > 0 else '')
    df = df[['ID', 'Date', 'News Text', 'Source URL', 'tags', 'Source', 'External URL']]
    return df


def news(db_path):
    return load_db(db_path)
