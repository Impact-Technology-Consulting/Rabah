from datetime import timedelta

from celery import shared_task
from dateutil.relativedelta import relativedelta

from rabah_events.models import Event
from rabah_members.models import Member
from rabah_organisations.models import Group
from users.models import User


@shared_task
def create_event_for_repeat_count(event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event.parent_event:
        return False

    if event.repeat_end != "AFTER":
        return False

    for counter in range(event.repeat_count - 1):
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

        new_event = Event.objects.create(
            organisation=event.organisation,
            name=event.name,
            image=event.image,
            description=event.description,
            repeat=event.repeat,
            repeat_end=event.repeat_end,
            start_date=event.start_date,
            end_date=event.end_date,
            repeat_count=event.repeat_count,
            repeat_until_date=event.repeat_until_date,
        )

    return True


@shared_task
def create_event_for_until_date(event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event.parent_event:
        return False

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

        new_event = Event.objects.create(
            organisation=event.organisation,
            name=event.name,
            image=event.image,
            description=event.description,
            repeat=event.repeat,
            repeat_end=event.repeat_end,
            start_date=event.start_date,
            end_date=event.end_date,
            repeat_count=event.repeat_count,
            repeat_until_date=event.repeat_until_date,
        )
        if event.repeat_until_date and new_event.end_date.date() >= event.repeat_until_date:
            break
    return True


@shared_task
def create_multiple_members(data, organisation_id, groups):
    for item in data:

        user = User.objects.filter(email=item.get("email")).first()
        if user:
            continue
        if not item.get("email"):
            continue

        user = User.objects.create(
            email=item.get('email'),
            first_name=item.get('firstname', ""),
            last_name=item.get('lastname', ""),
            mobile=item.get('mobile')
        )
        try:
            instance = Member()
            user_profile = user.user_profile
            user_profile.address = item.get('address')
            user_profile.career = item.get('career')
            user_profile.gender = f"{item.get('gender')}".upper()
            user_profile.save()
            instance.organisation_id = organisation_id
            instance.user = user
            instance.save()

            for group_data in groups:
                group = Group.objects.filter(id=group_data.get("id")).first()
                if group:
                    instance.groups.add(group)

            instance.save()

        except:
            user.delete()
    return True
