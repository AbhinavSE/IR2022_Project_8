import pandas as pd
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import io
import os
import json


def log(text):
    print(text)


def get_file_list(drive, folder_id):
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    return file_list


def to_df(string):
    print('Converting to df')
    return pd.read_csv(io.StringIO(string), low_memory=False)


def get_json_from_drive(path, drive=None):
    print(f'Getting {path} from drive')
    if drive is None:
        drive = authenticate_drive()
    f_id = '1blVhhVVAOYxYvxWxavh6bGdjbf0IFtGR'
    for f in path.split('/'):
        for f2 in get_file_list(drive, f_id):
            if f2['title'] == f:
                f_id = f2['id']
                break
    json_file = drive.CreateFile({'id': f_id})
    json_content = json.loads(json_file.GetContentString())
    return json_content, f_id


def get_csv_from_drive(path, drive=None):
    print(f'Getting {path} from drive')
    if drive is None:
        drive = authenticate_drive()
    f_id = '1blVhhVVAOYxYvxWxavh6bGdjbf0IFtGR'
    if path != '/':
        for f in path.split('/'):
            for f2 in get_file_list(drive, f_id):
                if f2['title'] == f:
                    f_id = f2['id']
                    break
    df = None
    if path[-4:] != '.csv':
        df = pd.DataFrame()
        for f in get_file_list(drive, f_id):
            new_path = os.path.join(path, f['title'])
            df = df.append(get_csv_from_drive(new_path, drive)[0], ignore_index=True)
    else:
        csv = drive.CreateFile({'id': f_id})
        df = to_df(csv.GetContentString())
    print(len(df))
    return df, f_id


def upload_json(js, js_id, drive=None):
    print('Uploading json')
    if drive is None:
        drive = authenticate_drive()
    with open('/tmp/temp_{js_id}.json', 'w') as f:
        json.dump(js, f, indent=4)
    file1 = drive.CreateFile({'id': js_id})
    file1.SetContentFile('/tmp/temp_{js_id}.json')
    file1.Upload()
    os.remove('/tmp/temp_{js_id}.json')


def upload_csv(df, df_id, drive=None):
    print('Uploading csv')
    if drive is None:
        drive = authenticate_drive()
    df.to_csv('/tmp/temp_{df_id}.csv', index=False)
    file1 = drive.CreateFile({'id': df_id})
    file1.SetContentFile('/tmp/temp_{df_id}.csv')
    file1.Upload()
    os.remove('/tmp/temp_{df_id}.csv')


def create_folder(path, drive=None):
    if drive is None:
        drive = authenticate_drive()
    # Create folder in drive path
    folder_metadata = {
        'title': path,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']


def authenticate_drive():
    print('authenticating to drive')
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'utils/drive/drive_creds.json', scope)
    drive = GoogleDrive(gauth)
    return drive
