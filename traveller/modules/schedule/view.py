from datetime import date, datetime
from flask import flash

from shopyo.api.module import ModuleHelp
from modules.conf.models import Conf
from modules.schedule.models import Schedule
from modules.schedule.models import Day
from modules.schedule.models import Activity
from modules.schedule.forms import DayForm
from modules.schedule.forms import NormalActivityForm
from modules.schedule.forms import TalkActivityForm
from shopyo.api.html import notify_danger

# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


@module_blueprint.route("/<int:year>/day/", methods=["POST"])
def add_day(year):
    conf = Conf.query.filter(
            Conf.year==year
        ).first()

    if conf.schedule is None:
        conf.schedule = Schedule()

    form = DayForm()
    form.validate()

    if form.date.data < date.today():
        flash(notify_danger("new schedule date should be today or later"))
        return mhelp.redirect_url('y.schedule', year=year)

    day = Day(
        date=form.date.data
        )
    conf.schedule.days.append(day)
    conf.update()
    return mhelp.redirect_url('y.schedule', year=year)


@module_blueprint.route("/<int:year>/day/<day_id>/<act_type>", methods=["POST"])
def add_activity(year, day_id, act_type):
    if act_type == 'normal_activity':
        day = Day.query.get(day_id)
        form = NormalActivityForm()
        form.validate()
        if form.end_time.data < form.start_time.data:
            flash(notify_danger("End time should be greater than start date"))
            return mhelp.redirect_url('y.schedule', year=year)
        activity = Activity()
        form.populate_obj(activity)
        activity.type = 'normal_activity'
        day.activities.append(activity)
        day.update()
    elif act_type == 'talk':
        day = Day.query.get(day_id)
        form = TalkActivityForm()

        form.validate()
        if form.end_time.data < form.start_time.data:
            flash(notify_danger("End time should be greater than start date"))
            return mhelp.redirect_url('y.schedule', year=year)
        activity = Activity()
        # form.populate_obj(activity)
        activity.start_time = form.start_time.data
        activity.end_time = form.end_time.data
        activity.type = 'talk'
        activity.talk_id = form.talks.data.id
        day.activities.append(activity)
        day.update()

    return mhelp.redirect_url('y.schedule', year=year)


@module_blueprint.route("/<int:year>/act/<act_id>/edit/<act_type>", methods=["POST"])
def edit_activity(year, act_id, act_type):
    if act_type == 'normal_activity':
        form = NormalActivityForm()
        form.validate()
        if form.end_time.data < form.start_time.data:
            flash(notify_danger("End time should be greater than start date"))
            return mhelp.redirect_url('y.schedule', year=year)
        activity = Activity.query.get(act_id)
        form.populate_obj(activity)
        activity.update()
    elif act_type == 'talk':
        form = TalkActivityForm()
        form.validate()
        if form.end_time.data < form.start_time.data:
            flash(notify_danger("End date should be greater than start date"))
            return mhelp.redirect_url('y.schedule', year=year)
        activity = Activity.query.get(act_id)
        form.populate_obj(activity)
        activity.update()
    return mhelp.redirect_url('y.schedule', year=year)


@module_blueprint.route("/<int:year>/act/<act_id>/delete", methods=["GET"])
def delete_activity(year, act_id):
    activity = Activity.query.get(act_id)
    activity.delete()
    return mhelp.redirect_url('y.schedule', year=year)

# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
