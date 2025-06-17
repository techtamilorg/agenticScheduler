from abc import ABC, abstractmethod
from typing import List, Dict, Any

event_schema = {
    "id": str,
    "title": str,
    "start_time": str,
    "end_time": str,
    "location": str,
    "attendees": List[str],
    "recurrence": Dict[str, Any]
}

class CalendarProvider(ABC):
    @abstractmethod
    def create_event(self, event: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_event(self, event_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_event(self, event_id: str, updated_event: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_event(self, event_id: str) -> bool:
        pass

    @abstractmethod
    def search_events(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
