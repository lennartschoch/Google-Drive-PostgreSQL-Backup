from __future__ import print_function
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from datetime import date
from oauth2client import file
from dotenv import load_dotenv
from pathlib import Path

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():

    load_dotenv()

    # Create database dump and save it to backup.gz
    os.system('pg_dump -h localhost -U %s %s | gzip > %s/backup.gz' % (os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_DATABASE'), Path.home()))

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        print('Error logging into Google Drive API')
        exit(1)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    full_date = str(date.today())
    year = full_date.split('-')[0]
    month = full_date.split('-')[1]

    # Find or create folder for current year

    response = service.files().list(q=("mimeType='application/vnd.google-apps.folder' " +
                                       "and '%s' in parents " +
                                       "and name = '%s'")
                                    % (os.getenv('DRIVE_ROOT_FOLDER_ID'), year),
                                    spaces='drive',
                                    fields='nextPageToken, files(id)').execute()
    year_folders = response.get('files', [])
    if len(year_folders) > 0:
        year_folder = year_folders[0].get('id')
    else:
        file_metadata = {
            'name': year,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [os.getenv('DRIVE_ROOT_FOLDER_ID')]
        }
        year_folder = service.files().create(body=file_metadata,
                                             fields='id').execute()
        year_folder = year_folder.get('id')

    # Find or create Folder for current month

    response = service.files().list(
        q="mimeType='application/vnd.google-apps.folder' and '%s' in parents and name = '%s'"
          % (year_folder, month),
        spaces='drive',
        fields='nextPageToken, files(id)').execute()
    month_folders = response.get('files', [])
    if len(month_folders) > 0:
        month_folder = month_folders[0].get('id')
    else:
        file_metadata = {
            'name': month,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [year_folder]
        }
        month_folder = service.files().create(body=file_metadata,
                                              fields='id').execute()
        month_folder = month_folder.get('id')

    # Upload backup to folder

    file_metadata = {'name': ('%s.gz' % full_date),
                     'parents': [month_folder]
                     }
    media = MediaFileUpload('%s/backup.gz' % Path.home(),
                            mimetype='application/gzip')
    service.files().create(body=file_metadata,
                           media_body=media,
                           fields='id').execute()

    # Remove local backup file
    os.system('rm %s/backup.gz' % Path.home())


if __name__ == '__main__':
    main()