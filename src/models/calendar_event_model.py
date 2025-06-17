from typing import Dict, Any

class CalendarEventModel:
    def parse(self, user_input: str) -> Dict[str, Any]:
        # Stub: Replace with real LLM call
        return {
            'attendees': ['alice@example.com', 'bob@example.com'],
            'time_preferences': {
                'date_range': ['2025-06-18', '2025-06-20'],
                'time_range': ['09:00', '17:00'],
                'duration_minutes': 30
            },
            'timezone_info': {
                'requester': 'America/Toronto',
                'attendees': {
                    'alice@example.com': 'America/New_York',
                    'bob@example.com': 'Europe/London'
                }
            },
            'title': 'Product Demo Sync',
            'location': 'Zoom',
            'video_conference': True
        }