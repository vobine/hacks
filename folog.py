"""Hacking foodlog.  Read-only spreadsheet access.
Partly lifted from Google API quickstart.py."""

import httplib2
import os
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Food log hackery'

class Folog:
    """Food logging."""

    def __init__ (self,
                  scopes=SCOPES,
                  secret=CLIENT_SECRET_FILE,
                  application=APPLICATION_NAME,
                  spreadsheetId='1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'):
        """Set up context for spreadsheet queries."""

        # Locate files with credentials.
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        # Prepare credentials for authorization.
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(secret, scopes)
            flow.user_agent = application
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        self.credentials =  credentials

        # Authorize with OAuth2.
        http = self.credentials.authorize(httplib2.Http())

        # Prepare resource discovery.
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)

        # Get spreadsheet summary metadata.
        self.spreadsheets = self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheetId).execute()

    def get (self):
        rangeName = 'Class Data!A2:E'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        self.values = result.get('values', [])
