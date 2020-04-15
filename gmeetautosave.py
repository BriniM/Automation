from __future__ import print_function
import datetime
import pickle
import os.path
import threading
import json

from selenium import webdriver
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pyrfc3339 import parse
from time import sleep
from datetime import datetime, timezone

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

DRIVER = None

file_handle = open('meet links.txt', 'r')
MEET_LINKS = json.loads(file_handle.read())
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


def start_recording(subject):
    global DRIVER
    DRIVER = webdriver.Chrome()
    DRIVER.get(MEET_LINKS[subject])

    # Mic and webcam off.
    # Tap Mic: //*[@id="yDmH0d"]/c-wiz/div/div/div[3]/div[3]/div/div[2]/div/div[1]/div[4]/div[1]/div/div/div
    # Tap Cam: //*[@id="yDmH0d"]/c-wiz/div/div/div[3]/div[3]/div/div[2]/div/div[1]/div[4]/div[2]/div/div
    # Tap Join: //*[@id="yDmH0d"]/c-wiz/div/div/div[3]/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/span
    # SHIFT + PrtScreen, Click on the region to start recording with ShareX


def end_recording():
    # SHIFT + PrtScreen

    global DRIVER
    DRIVER.close()
    pass


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

            threading.Timer(delay_to_start, start_recording, event['description']).start()
            threading.Timer(delay_to_end, end_recording).start()

        # Fetch new events when the ones we've set have finished execution
        while len(threading.enumerate()) != 4:
            sleep(60)
