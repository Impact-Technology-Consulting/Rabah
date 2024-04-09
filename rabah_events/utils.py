from datetime import timedelta

from dateutil.relativedelta import relativedelta

from rabah_events.models import Event


def check_event_creation_limit(event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event.parent_event:
        return False

    event_count = 0  # Counter for the number of events that would be created

    if event.repeat_end != "ON_DATE":
        return False

    while True:
        if event.repeat == "DAILY":
            # For daily repetition, update start_date and end_date to the next day
            event.start_date += timedelta(days=1)
            event.end_date += timedelta(days=1)
        elif event.repeat == "WEEKLY":
            # For weekly repetition, update start_date and end_date to the same day of the next week
            event.start_date += timedelta(weeks=1)
            event.end_date += timedelta(weeks=1)
        elif event.repeat == "MONTHLY":
            # For monthly repetition, update start_date and end_date to the same day of the next month
            event.start_date += relativedelta(months=1)
            event.end_date += relativedelta(months=1)
        elif event.repeat == "YEARLY":
            # For yearly repetition, update start_date and end_date to the same day of the next year
            event.start_date += relativedelta(years=1)
            event.end_date += relativedelta(years=1)

        event_count += 1
        if event_count > 100:
            # If the number of events to be created exceeds 100, return False
            return False
        if event.repeat_until_date and event.end_date.date() >= event.repeat_until_date:
            break
    return True
