from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# This is basically the quickstart code from the documentation.
# Run this script whenever you'll need to get a new API token from Google.

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        print('Credentials saved.')
    else:
        print('Credentials seem to be valid. Remove credentials.json to renew them anyways.')


if __name__ == '__main__':
    main()