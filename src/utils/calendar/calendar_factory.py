from utils.calendar.calendar_provider import CalendarProvider
from utils.calendar.calendar_google import GoogleCalendarProvider

def get_calendar_provider(provider_name: str) -> CalendarProvider:
    if provider_name == "google":
        return GoogleCalendarProvider()
    raise ValueError("Unsupported provider")