import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, ANY
from utils.calendar.calendar_google import GoogleCalendarProvider

# -----------------------------
# Fixtures & Helpers
# -----------------------------

@pytest.fixture
def sample_event():
    now = datetime.utcnow()
    return {
        "title": "Team Sync Meeting",
        "start_time": (now + timedelta(hours=1)).isoformat(),
        "end_time": (now + timedelta(hours=2)).isoformat(),
        "location": "Google Meet (auto-generated)",
        "attendees": ["testuser@example.com"],
        "recurrence": {},
        "timeZone": "UTC"
    }

def create_mock_service(mocker):
    """Helper to create a mock Google Calendar service structure."""
    mock_service = MagicMock()
    mock_events = MagicMock()
    mock_service.events.return_value = mock_events
    return mock_service, mock_events


# -----------------------------
# Test Cases
# -----------------------------

def test_create_event(mocker, sample_event):
    mock_service, mock_events = create_mock_service(mocker)
    mocker.patch('utils.calendar.calendar_google.GoogleCalendarProvider.authenticate', return_value=mock_service)
    provider = GoogleCalendarProvider()

    mock_insert_request = MagicMock()
    mock_events.insert.return_value = mock_insert_request
    mock_insert_request.execute.return_value = {'id': 'mock_event_id_123'}

    event_id = provider.create_event(sample_event)

    mock_events.insert.assert_called_once_with(
        calendarId='primary',
        body=ANY,
        conferenceDataVersion=1
    )
    assert event_id == 'mock_event_id_123'


def test_get_event(mocker):
    mock_service, mock_events = create_mock_service(mocker)
    mocker.patch('utils.calendar.calendar_google.GoogleCalendarProvider.authenticate', return_value=mock_service)
    provider = GoogleCalendarProvider()

    mock_get_request = MagicMock()
    mock_events.get.return_value = mock_get_request
    mock_event_response = {
        'id': 'mock_event_id_abc',
        'summary': 'Fetched Event',
        'start': {'dateTime': '...', 'timeZone': 'UTC'},
        'end': {'dateTime': '...', 'timeZone': 'UTC'},
        'location': 'Mock Location',
        'attendees': [{'email': 'a@b.com'}],
        'conferenceData': {'conferenceId': 'mock-meet-id'}
    }
    mock_get_request.execute.return_value = mock_event_response

    event = provider.get_event('mock_event_id_abc')

    mock_events.get.assert_called_once_with(
        calendarId='primary',
        eventId='mock_event_id_abc'
    )
    assert event == mock_event_response


def test_update_event(mocker, sample_event):
    mock_service, mock_events = create_mock_service(mocker)
    mocker.patch('utils.calendar.calendar_google.GoogleCalendarProvider.authenticate', return_value=mock_service)
    provider = GoogleCalendarProvider()

    test_event_id = 'mock_event_id_update'
    original_event = {
        'id': test_event_id,
        'summary': 'Old Title',
        'start': {'dateTime': '...', 'timeZone': 'UTC'},
        'end': {'dateTime': '...', 'timeZone': 'UTC'},
        'location': 'Old Location',
        'attendees': [{'email': 'old@example.com'}],
        'conferenceData': {
            'conferenceId': 'abc',
            'entryPoints': [{'uri': 'https://meet.google.com/abc'}]
        }
    }

    updated_event_data = {
        "title": "New Title",
        "start_time": sample_event["start_time"],
        "end_time": sample_event["end_time"],
        "attendees": ["new@example.com"],
        "timeZone": "UTC"
    }

    mock_get_request = MagicMock()
    mock_events.get.return_value = mock_get_request
    mock_get_request.execute.return_value = original_event

    mock_update_request = MagicMock()
    mock_events.update.return_value = mock_update_request
    mock_update_request.execute.return_value = {'id': test_event_id}

    success = provider.update_event(test_event_id, updated_event_data)

    mock_events.get.assert_called_once_with(
        calendarId='primary',
        eventId=test_event_id
    )
    mock_events.update.assert_called_once_with(
        calendarId='primary',
        eventId=test_event_id,
        body=ANY,
        conferenceDataVersion=1
    )
    assert success is True


def test_delete_event(mocker):
    mock_service, mock_events = create_mock_service(mocker)
    mocker.patch('utils.calendar.calendar_google.GoogleCalendarProvider.authenticate', return_value=mock_service)
    provider = GoogleCalendarProvider()

    mock_delete_request = MagicMock()
    mock_events.delete.return_value = mock_delete_request
    mock_delete_request.execute.return_value = None

    success = provider.delete_event('mock_event_id_delete')

    mock_events.delete.assert_called_once_with(
        calendarId='primary',
        eventId='mock_event_id_delete'
    )
    assert success is True


def test_search_events(mocker):
    mock_service, mock_events = create_mock_service(mocker)
    mocker.patch('utils.calendar.calendar_google.GoogleCalendarProvider.authenticate', return_value=mock_service)
    provider = GoogleCalendarProvider()

    mock_list_request = MagicMock()
    mock_events.list.return_value = mock_list_request
    mock_list_request.execute.return_value = {
        'items': [
            {'id': 'id1', 'summary': 'Meeting 1'},
            {'id': 'id2', 'summary': 'Another Meeting'}
        ]
    }

    search_criteria = {"keyword": "Meeting"}
    results = provider.search_events(search_criteria)

    mock_events.list.assert_called_once_with(
        calendarId='primary',
        q='Meeting'
    )
    assert results == [
        {'id': 'id1', 'summary': 'Meeting 1'},
        {'id': 'id2', 'summary': 'Another Meeting'}
    ]
