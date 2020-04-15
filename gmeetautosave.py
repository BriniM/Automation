# Google Example Imports
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# End Google Imports

import json
import threading
import webbrowser  # Should be replaced by Selenium
import win32api  # Could use pyautogui instead of these 3 imports
import win32con
import keyboard

from pyrfc3339 import parse
from time import sleep
from datetime import datetime, timezone

file_handle = open('meet links.txt', 'r')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
if file_handle:
    MEET_LINKS = json.loads(file_handle.read())
else:
    print('Error parsing Meet Links file.')
    exit()

file_handle.close()


class GoogleCalendar:
    def __init__(self):
        self.creds = None
        self.service = None

    def authorize(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_events(self):
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # Get the upcoming 10 events
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def start_recording(subject):
    # TODO: Selenium + Cookies.
    webbrowser.open('https://' + MEET_LINKS[subject])
    # Give the browser plenty of time to load the page
    sleep(20)
    # Mic and webcam off
    click(410, 627)
    sleep(1)
    click(489, 627)
    sleep(1)
    # Tap Join
    click(992, 462)
    # SHIFT + PrtScreen, Click on the region to start recording with ShareX
    keyboard.press_and_release('shift + print screen')
    sleep(1)
    click(992, 462)


def end_recording():
    keyboard.press_and_release('shift + print screen')


if __name__ == "__main__":
    gc = GoogleCalendar()
    gc.authorize()
    events = gc.get_events()

    while True:
        # Setup the timers
        for event in events:
            now = datetime.now(timezone.utc)
            start = parse(event['start']['dateTime'])
            end = parse(event['end']['dateTime'])

            # Delay to start + 3 minutes.
            delay_to_start = (start - now).total_seconds() + 180
            # Delay to end + 30 minutes.
            delay_to_end = (end - now).total_seconds() + 1800

            threading.Timer(delay_to_start, start_recording, args=[event['description']]).start()
            threading.Timer(delay_to_end, end_recording).start()

        # Fetch new events when the ones we've set have finished execution
        while len(threading.enumerate()) != 4:
            sleep(60)
