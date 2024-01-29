from django.urls import path

from .views import EventView, EventCalendarView, EventDeleteView, \
    MarkAttendancePageView, UpdateOrCreateMemberAttendanceView

app_name = "rabah_events"
urlpatterns = [
    path("", EventView.as_view(), name="events"),
    path("event_calendar", EventCalendarView.as_view(), name="event_calendar"),
    path("mark_attendance/<str:event_id>/", MarkAttendancePageView.as_view(), name="mark_attendance"),
    path("update_or_create_attendance/", UpdateOrCreateMemberAttendanceView.as_view(),
         name="update_or_create_attendance"),
    path("event_delete/<str:event_id>/", EventDeleteView.as_view(), name="event_delete"),

]
