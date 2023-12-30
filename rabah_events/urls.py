from django.urls import path

from .views import EventView, EventCalendarView, EventDeleteView

app_name = "rabah_events"
urlpatterns = [
    path("", EventView.as_view(), name="events"),
    path("event_calendar", EventCalendarView.as_view(), name="event_calendar"),
    path("event_delete/<str:event_id>/", EventDeleteView.as_view(), name="event_delete"),

]
