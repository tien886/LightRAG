"""Backend endpoint enum values used by chat lookup planner and executor."""
from __future__ import annotations

from enum import Enum


class BackendEndpoint(str, Enum):
    USER_PROFILE             = "user_profile"
    SCHEDULE_DEADLINE_GET    = "schedule_deadline_get"
    SCHEDULE_DEADLINE_CREATE = "schedule_deadline_create"
    SCHEDULE_CALENDAR        = "schedule_calendar"
    DOCUMENT_SHARED          = "document_shared_with_me"
    DOCUMENT_SEARCH          = "document_search"
    DOCUMENT_DOWNLOAD        = "document_download"

    @classmethod
    def values(cls) -> set[str]:
        return {item.value for item in cls}
