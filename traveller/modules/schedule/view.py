from datetime import date, datetime, tzinfo
import re

from init import conf_time_zone
from shopyo.api.module import ModuleHelp
from modules.conf.models import Conf
from modules.schedule.models import Schedule
from modules.schedule.models import Day
from modules.schedule.models import Activity
from modules.schedule.forms import DayForm
from modules.schedule.forms import NormalActivityForm
from modules.schedule.forms import TalkActivityForm
from modules.schedule.helper import get_calendar

from helpers.c2021.notif import alert_success
from helpers.c2021.notif import alert_danger

from flask_login import login_required
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

# from flask import render_template
# from flask import url_for
# from flask import redirect
from flask import request, abort

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
def index():
    return mhelp.info["display_string"]


@module_blueprint.route("/<int:year>/day/", methods=["POST"])
def add_day(year):
    if current_user.is_admin:
        conf = Conf.query.filter(Conf.year == year).first()

        if conf.schedule is None:
            conf.schedule = Schedule()

        form = DayForm()
        if not form.validate():
            alert_danger("Day not added!")
            return mhelp.redirect_url("y.schedule", year=year)

        if form.date.data < date.today():
            alert_danger("New schedule date should be today or later")
            return mhelp.redirect_url("y.schedule", year=year)

        day = Day(date=form.date.data)

        conf.schedule.days.append(day)
        conf.update()
    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/day/<day_id>/<act_type>", methods=["POST"])
def add_activity(year, day_id, act_type):
    if act_type == "normal_activity":
        day = Day.query.get(day_id)

        if day is None:
            alert_danger("Invalid day.")
            return mhelp.redirect_url("y.schedule", year=year)
        form = NormalActivityForm()

        if not form.validate():
            alert_danger("Activity not added!")
            return mhelp.redirect_url("y.schedule", year=year)

        if form.end_time.data < form.start_time.data:
            alert_danger("End time should be greater than start date")
            return mhelp.redirect_url("y.schedule", year=year)

        # Check to ensure both start and end time are between 09:00 to 18:00
        activity_time_check = [
            True
            for i in (form.start_time.data, form.end_time.data)
            if "09:00:00" <= str(i) <= "18:00:00"
        ]
        if len(activity_time_check) != 2:
            alert_danger("Provide valid values for both start and end time.")
            return mhelp.redirect_url("y.schedule", year=year)

        # Convert both the start and end times with the default time zone for the conference
        activity_start = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.start_time.data).split(":")[0]),
            int(str(form.start_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )
        activity_end = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.end_time.data).split(":")[0]),
            int(str(form.end_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )

        activity = Activity()
        form.populate_obj(activity)
        activity.type = "normal_activity"
        activity.start_time = activity_start
        activity.end_time = activity_end
        day.activities.append(activity)
        day.update()
    elif act_type == "talk":
        day = Day.query.get(day_id)
        if day is None:
            alert_danger("Invalid day.")
            return mhelp.redirect_url("y.schedule", year=year)
        form = TalkActivityForm()

        if not form.validate():
            alert_danger("Activity not added!")
            return mhelp.redirect_url("y.schedule", year=year)
        if form.end_time.data < form.start_time.data:
            alert_danger("End time should be greater than start date")
            return mhelp.redirect_url("y.schedule", year=year)

        # Check to ensure both start and end time are between 09:00 to 18:00
        activity_time_check = [
            True
            for i in (form.start_time.data, form.end_time.data)
            if "09:00:00" <= str(i) <= "18:00:00"
        ]
        if len(activity_time_check) != 2:
            alert_danger("Provide valid values for both start and end time.")
            return mhelp.redirect_url("y.schedule", year=year)

       # Convert both the start and end times with the default time zone for the conference
        activity_start = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.start_time.data).split(":")[0]),
            int(str(form.start_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )
        activity_end = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.end_time.data).split(":")[0]),
            int(str(form.end_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )

        activity = Activity()
        # form.populate_obj(activity)
        activity.start_time = activity_start
        activity.end_time = activity_end
        activity.type = "talk"
        activity.talk_id = form.talks.data.id if form.talks.data is not None else None
        day.activities.append(activity)
        day.update()

    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/act/<act_id>/edit/<act_type>", methods=["POST"])
def edit_activity(year, act_id, act_type):
    if act_type == "normal_activity":
        form = NormalActivityForm()
        if not form.validate():
            alert_danger("Activity not edited!")
            return mhelp.redirect_url("y.schedule", year=year)
        if form.end_time.data < form.start_time.data:
            alert_danger("End time should be greater than start date")
            return mhelp.redirect_url("y.schedule", year=year)

        # Check to ensure both start and end time are between 09:00 to 18:00
        activity_time_check = [
            True
            for i in (form.start_time.data, form.end_time.data)
            if "09:00:00" <= str(i) <= "18:00:00"
        ]
        if len(activity_time_check) != 2:
            alert_danger("Provide valid values for both start and end time.")
            return mhelp.redirect_url("y.schedule", year=year)

        activity = Activity.query.get(act_id)
        day = Day.query.get(activity.day_id)

        # Convert both the start and end times with the default time zone for the conference
        activity_start = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.start_time.data).split(":")[0]),
            int(str(form.start_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )
        activity_end = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.end_time.data).split(":")[0]),
            int(str(form.end_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )
        if activity is None:
            alert_danger("Invalid activity.")
            return mhelp.redirect_url("y.schedule", year=year)
        # form.populate_obj(activity)
        activity.start_time = activity_start
        activity.end_time = activity_end
        activity.update()
    elif act_type == "talk":
        form = TalkActivityForm()
        if not form.validate():
            alert_danger("Activity not edited!")
            return mhelp.redirect_url("y.schedule", year=year)

        if form.end_time.data < form.start_time.data:
            alert_danger("End date should be greater than start date")
            return mhelp.redirect_url("y.schedule", year=year)

        # Check to ensure both start and end time are between 09:00 to 18:00
        activity_time_check = [
            True
            for i in (form.start_time.data, form.end_time.data)
            if "09:00:00" <= str(i) <= "18:00:00"
        ]
        if len(activity_time_check) != 2:
            alert_danger("Provide valid values for both start and end time.")
            return mhelp.redirect_url("y.schedule", year=year)

        activity = Activity.query.get(act_id)
        day = Day.query.get(activity.day_id)

        # Convert both the start and end times with the default time zone for the conference
        activity_start = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.start_time.data).split(":")[0]),
            int(str(form.start_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )
        activity_end = datetime(
            int(str(day.date).split("-")[0]),
            int(str(day.date).split("-")[1]),
            int(str(day.date).split("-")[2]),
            int(str(form.end_time.data).split(":")[0]),
            int(str(form.end_time.data).split(":")[1]),
            tzinfo=conf_time_zone,
        )

        if activity is None:
            alert_danger("Invalid activity.")
            return mhelp.redirect_url("y.schedule", year=year)

        activity.talk_id = form.talks.data.id if form.talks.data is not None else None
        activity.start_time = activity_start
        activity.end_time = activity_end
        activity.update()
    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/day/<day_id>/edit", methods=["POST"])
def edit_day(year, day_id):
    if current_user.is_admin:
        day = Day.query.get(day_id)

        if day is None:
            alert_danger("Invalid day.")
            return mhelp.redirect_url("y.schedule", year=year)
        try:
            form = DayForm(obj=day)
            form.populate_obj(day)
            if not form.validate():
                alert_danger("Day not edited!")
                return mhelp.redirect_url("y.schedule", year=year)

            if form.date.data < date.today():
                alert_danger("New schedule date should be today or later")
                return mhelp.redirect_url("y.schedule", year=year)

            day.update()
            alert_success("Day edited!")
        except IntegrityError:
            alert_danger("Day not edited!")
    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/act/<act_id>/delete")
def delete_activity(year, act_id):
    if not current_user.is_admin:
        alert_danger("You don't have access to delete activity.")
        return mhelp.redirect_url("y.schedule", year=year)
    activity = Activity.query.get(act_id)
    if activity is None:
        alert_danger("Invalid activity.")
        return mhelp.redirect_url("y.schedule", year=year)
    activity.delete()
    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/day/<day_id>/delete")
@login_required
def delete_day(year, day_id):
    if not current_user.is_admin:
        alert_danger("You don't have access to delete days!")
        return mhelp.redirect_url("y.schedule", year=year)

    day = Day.query.get(day_id)
    if day is None:
        alert_danger("Invalid day.")
        return mhelp.redirect_url("y.schedule", year=year)
    day.delete()
    alert_success("Day deleted!")
    return mhelp.redirect_url("y.schedule", year=year)


@module_blueprint.route("/<int:year>/calendar/<tz>")
def calendar(year, tz):
    get_all_activities = request.args.get('all', False, type=bool)
    activity_id = request.args.get('act_id', None, type=int)
    if tz is None or tz.strip() == '':
        tzname = 'UTC'
    else:
        tzname = tz #.replace('/', '_')
    
    if get_all_activities is True:
        return mhelp.redirect_url("schedule.all_activities_cal", _year=year, tz=tzname)
    act_id = Activity.query.get(activity_id)
    if get_all_activities is False and act_id is not None:
        return mhelp.redirect_url("schedule.single_activity_cal", _year=year, act_id= activity_id, tz=tzname)
    
    return mhelp.redirect_url("y.schedule", year=year)
    

@module_blueprint.route("/download_ical/<string:_year>_events.ics")
def all_activities_cal(_year):
    tzname = request.args.get('tz')
    output = get_calendar(timezone=tzname, conf_year=_year, all=True)
    return output


@module_blueprint.route("/download_ical/<string:_year>_activity_<int:act_id>.ics")
def single_activity_cal(_year, act_id):
    tzname = request.args.get('tz')
    output = get_calendar(timezone=tzname, conf_year=_year, activity_id=act_id)
    return output