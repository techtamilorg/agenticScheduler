from datetime import datetime, timedelta
from utils.calendar.calendar_factory import get_calendar_provider



def main():
    provider = get_calendar_provider("google")

    now = datetime.utcnow()
    sample_event = {
        "title": "Team Sync Meeting",
        "start_time": (now + timedelta(hours=1)).isoformat() + "Z",
        "end_time": (now + timedelta(hours=2)).isoformat() + "Z",
        "location": "Google Meet (auto-generated)",
        "attendees": ["testuser@example.com"],
        "recurrence": {}
    }

    print("Creating event...")
    event_id = provider.create_event(sample_event)
    print(f"Event created with ID: {event_id}")
    
    print("Fetching event...")
    event = provider.get_event(event_id)
    print(f"Fetched event: {event}")
    
    if event.get('hangoutLink'):
        print(f"Google Meet Link: {event.get('hangoutLink')}")
    if event.get('conferenceData'):
        print(f"Conference Data: {event.get('conferenceData')}")
        
    print("Updating event title...")
    sample_event["title"] = "Updated Team Sync"
    updated = provider.update_event(event_id, sample_event)
    print(f"Event updated: {updated}")

    if updated:
        print("Fetching event again after update...")
        event_after_update = provider.get_event(event_id)
        print(f"Fetched event after update: {event_after_update}")
        if event_after_update.get('hangoutLink'):
            print(f"Google Meet Link after update: {event_after_update.get('hangoutLink')}")
        if event_after_update.get('conferenceData'):
            print(f"Conference Data after update: {event_after_update.get('conferenceData')}")

    print("Searching events with keyword 'Team'...")
    results = provider.search_events({"keyword": "Team"})
    for evt in results:
        print(f"Found: {evt.get('summary')} (ID: {evt.get('id')})")


if __name__ == '__main__':
    main()
