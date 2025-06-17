from utils.calendar.calendar_provider import CalendarProvider, event_schema
from typing import Dict, Any, List
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import uuid
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarProvider(CalendarProvider):
    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('calendar', 'v3', credentials=creds)

    def create_event(self, event: Dict[str, Any]) -> str:
        event_body = {
            'summary': event['title'],
            'start': {'dateTime': event['start_time'], 'timeZone': 'UTC'},
            'end': {'dateTime': event['end_time'], 'timeZone': 'UTC'},
            'location': event.get('location', ''),
            'attendees': [{'email': a} for a in event.get('attendees', [])],
            'conferenceData': {
                'createRequest': {
                    'requestId': f"{uuid.uuid4().hex}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
        }

        created_event = self.service.events().insert(
            calendarId='primary',
            body=event_body,
            conferenceDataVersion=1
        ).execute()

        return created_event['id']


    def get_event(self, event_id: str) -> Dict[str, Any]:
        return self.service.events().get(calendarId='primary', eventId=event_id).execute()

    def update_event(self, event_id: str, updated_event: Dict[str, Any]) -> bool:
        existing_event = self.get_event(event_id)

        event_body = {
            'summary': updated_event['title'],
            'start': {'dateTime': updated_event['start_time'], 'timeZone': 'UTC'},
            'end': {'dateTime': updated_event['end_time'], 'timeZone': 'UTC'},
            'location': updated_event.get('location', existing_event.get('location', '')),
            'attendees': [{'email': a} for a in updated_event.get('attendees', [])],
        }

        if 'conferenceData' in updated_event:
            if updated_event['conferenceData'] is not None:
                event_body['conferenceData'] = updated_event['conferenceData']
        elif 'conferenceData' in existing_event:
            event_body['conferenceData'] = existing_event['conferenceData']

        params = {'calendarId': 'primary', 'eventId': event_id, 'body': event_body}
        if event_body.get('conferenceData') is not None:
            params['conferenceDataVersion'] = 1

        updated = self.service.events().update(**params).execute()
        return updated.get('id') == event_id

    def delete_event(self, event_id: str) -> bool:
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True

    def search_events(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self.service.events().list(calendarId='primary', q=criteria.get("keyword", "")).execute()
        return result.get('items', [])