from datetime import datetime as dt
from typing import List

from icalendar import Calendar, Event, vCalAddress, vText, vUri, Timezone
try:
    from zoneinfo import ZoneInfoNotFoundError
except ImportError:
    from backports.zoneinfo import ZoneInfoNotFoundError
    
from init import conf_time_zone, tzinfo
from modules.schedule.models import Day
from modules.schedule.models import Activity


def get_calendar(timezone, conf_year, all=False, activity_id=None) -> bytes:
    """
    get_calendar This method handles the creation of an iCal calendar for an activity or a list of activities.

    :param timezone: a timezone from the IANA timezone list.
    :param all: True or False, if True make iCalendar with all events.
    :param activity_id: ID of an activity, defaults to None.
    :return: a bytes string with details of the calendar.
    :rtype: bytes
    """
    timezone = timezone.replace('_', '/')
    if all is True:
        event_list = all_activities(timezone)
        return schedule_activities(event_list, timezone, conf_year)
    event_list = [activity(activity_id, timezone)]
    return schedule_activities(event_list, timezone, conf_year)


def schedule_activities(event_list, timezone, conf_year) -> bytes:
    """
    schedule_activities This method creates an ical calendar.

    :param event_list: events to be added to the calendar.
    :type event_list: list
    :param timezone: a timezone from the IANA timezone list.
    :return: a bytes string with details of the calendar.
    :rtype: bytes
    """
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', f"-//FLASKCON{conf_year}//flaskcon.com//")
    flaskcon_uri = vUri("https://flaskcon.com")
    cal.add('website', flaskcon_uri)
    tz = Timezone()
    tz.add('tzid', conf_time_zone)
    tz.add('conferencetimezone', conf_time_zone)
    tz.add('userstimezone', tzinfo(timezone))
    cal.add_component(tz)

    # Adding events to calendar
    for event in event_list:
        cal.add_component(event)

    # Adding custom properties
    organizer = vCalAddress('MAILTO:flaskcon@gmail.com')
    organizer.params['cn'] = vText('Abdur-Rahmaan Janhangeer')
    organizer.params['role'] = vText('Adminstrator')
    cal['organizer'] = organizer
    
    output = cal.to_ical(sorted=False)
    return output


def all_activities(timezone) -> List[Event]:
    """
    activity This method creates a list of events from the details of all activities.
    
    :param timezone: a timezone from the IANA timezone list.
    :return: an event
    :rtype: List[Event]
    """
    event_list = []
    activities = Activity.query.all()
    for act in activities:
        day = Day.query.get(act.day_id)

        end_datetime = dt.fromisoformat(f"{day.date} {act.end_time}")
        start_datetime = dt.fromisoformat(f"{day.date} {act.start_time}")
            
        ed_ = end_datetime.astimezone(tz=tzinfo(timezone))
        st_ = start_datetime.astimezone(tz=tzinfo(timezone))
        
        event = Event()
        
        if act.type == "normal_activity":
            event.add('summary', act.text)
            event.add('description', act.note)
            event.add('dtstart', st_)
            event.add('dtend', ed_)
            event.add('duration', ed_ - st_)
            talk_uri = vUri(f"https://flaskcon.com/y/2021/schedule/activity_{act.id}?tz={timezone}")
            event.add('url', talk_uri)
        elif act.type == "talk":
            talk = act.get_talk()
            authors_list = [f"{user.first_name} {user.last_name}" for user in talk.author_list.authors]
            authors = " ".join(authors_list)
            event.add('summary', f"{talk.title} by {authors.upper()}")
            event.add('description', talk.description)
            event.add('dtstart', st_)
            event.add('dtend', ed_)
            event.add('duration', ed_ - st_)
            talk_uri = vUri(f"https://flaskcon.com/y/2021/schedule/activity_{act.id}?tz={timezone}")
            event.add('url', talk_uri)
        
        event_list.append(event)
    return event_list


def activity(activity_id, timezone) -> Event:
    """
    activity This method creates an event by adding the details of an activity.

    :param timezone: a timezone from the IANA timezone list.
    :param activity_id: ID of an activity.
    :return: an event
    :rtype: Event
    """
    act = Activity.query.get(activity_id)
    day = Day.query.get(act.day_id)

    end_datetime = dt.fromisoformat(f"{day.date} {act.end_time}")
    start_datetime = dt.fromisoformat(f"{day.date} {act.start_time}")
        
    ed_ = end_datetime.astimezone(tz=tzinfo(timezone))
    st_ = start_datetime.astimezone(tz=tzinfo(timezone))
    
    event = Event()
    
    if act.type == "normal_activity":
        event.add('summary', act.text)
        event.add('description', act.note)
        event.add('dtstart', st_)
        event.add('dtend', ed_)
        event.add('duration', ed_ - st_)
        talk_uri = vUri(f"https://flaskcon.com/y/2021/schedule/activity_{activity_id}?tz={timezone}")
        event.add('url', talk_uri)
        return event
    elif act.type == "talk":
        talk = act.get_talk()
        authors_list = [f"{user.first_name} {user.last_name}" for user in talk.author_list.authors]
        authors = " ".join(authors_list)
        event.add('summary', f"{talk.title} by {authors.upper()}")
        event.add('description', talk.description)
        event.add('dtstart', st_)
        event.add('dtend', ed_)
        event.add('duration', ed_ - st_)
        talk_uri = vUri(f"https://flaskcon.com/y/2021/schedule/activity_{activity_id}?tz={timezone}")
        event.add('url', talk_uri)
        return event
