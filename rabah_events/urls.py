from django.urls import path

from .views import EventView, EventCalendarView, EventDeleteView, \
    MarkAttendancePageView, MarkMultipleMemberAttendanceView

app_name = "rabah_events"
urlpatterns = [
    path("", EventView.as_view(), name="events"),
    path("event_calendar", EventCalendarView.as_view(), name="event_calendar"),
    path("mark_attendance/<str:event_id>/", MarkAttendancePageView.as_view(), name="mark_attendance"),

    path("event_delete/<str:event_id>/", EventDeleteView.as_view(), name="event_delete"),
    path("mark_multiple_attendance/<str:event_id>/", MarkMultipleMemberAttendanceView.as_view(),
         name="mark_multiple_attendance"),

]
