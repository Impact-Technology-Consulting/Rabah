from django.urls import path

from .views import (
    EventView,
    EventListView,
    EventCalendarView,
    EventDeleteView,
    MarkAttendancePageView,
    MarkMultipleMemberAttendanceView,
    EventUpdateView,
)

app_name = "rabah_events"
urlpatterns = [
    path("", EventView.as_view(), name="events"),
    path(
        "event_update/<str:event_id>/", EventUpdateView.as_view(), name="event_update"
    ),
    path("event_list", EventListView.as_view(), name="event_list"),
    path("event_calendar", EventCalendarView.as_view(), name="event_calendar"),
    path(
        "mark_attendance/<str:event_id>/",
        MarkAttendancePageView.as_view(),
        name="mark_attendance",
    ),
    path(
        "event_delete/<str:event_id>/", EventDeleteView.as_view(), name="event_delete"
    ),
    path(
        "mark_multiple_attendance/<str:event_id>/",
        MarkMultipleMemberAttendanceView.as_view(),
        name="mark_multiple_attendance",
    ),
]
