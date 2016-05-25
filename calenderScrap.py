from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import pytz
from pprint import pprint

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MirrorMirror'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    return credentials


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # calculates the start and the end of today in UTC
    tz = pytz.timezone("America/Vancouver")
    today = datetime.datetime.now(tz)
    midnightPrev = today.replace(hour=00, minute=00, second=00, microsecond=000000)
    midnightPrev = midnightPrev.astimezone(pytz.timezone("utc")).isoformat()
    midnightNext = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    midnightNext = midnightNext.astimezone(pytz.timezone("utc")).isoformat()
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    midnightPrev2 = midnightPrev[:-6] + 'Z'
    midnightNext2 = midnightNext[:-6] + 'Z'

    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
            calendarId='lauriej.chang@gmail.com', timeMin=midnightPrev2, timeMax=midnightNext2, maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    #pprint(events)
    
    if not events:
        print('No upcoming events found.')
    for index, event in enumerate(events, start = 0):
        print(index, type(event))
        print(type(event['start']))
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
