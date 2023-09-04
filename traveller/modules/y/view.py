import json
from datetime import date
from shopyo.api.module import ModuleHelp
from flask import render_template
from modules.box__default.auth.models import User
from modules.conf.models import Conf
from modules.conf.models import Talk
from modules.conf.models import talk_list_author_bridge
from init import db
from modules.schedule.forms import DayForm
from modules.cfp.forms import SubmitTalkForm
from modules.schedule.models import Day, Schedule, Activity
from modules.schedule.forms import NormalActivityForm
from modules.schedule.forms import TalkActivityForm
from modules.profile.forms import UserProfileForm
from pathlib import Path
from flask import current_app
# from flask import url_for
# from flask import redirect
# from flask import flash

from flask import request
from flask_login import current_user
from flask_login import login_required

from helpers.c2021.notif import alert_success

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/<int:year>/")
def landing_page(year):
    context = mhelp.context()
    conf = Conf.query.filter(Conf.year == year).first_or_404()
    reviewers = conf.reviewer_list.reviewers if conf.reviewer_list is not None else None
    if reviewers is None:
        reviewers = []
    today = date.today()
    context.update(locals())

    staff_json = Path(current_app.root_path) / f'staff_{year}.json'
    if staff_json.exists():
        with open(staff_json) as f:
            staff = f.read()
        this_years_staff = json.loads(staff)
    else:
        this_years_staff = None

    return render_template('conftheme/{}/index.html'.format(year), this_years_staff=this_years_staff, **context)


@module_blueprint.route("/<int:year>/about")
def about(year):
    return render_template('conftheme/{}/parts/about_us.html'.format(year))


@module_blueprint.route("/<int:year>/contact")
def contact_page(year):
    return render_template('conftheme/{}/parts/contact_us.html'.format(year))


@module_blueprint.route("/<int:year>/cfp/")
@login_required
def cfp(year):
    context = mhelp.context()
    talk_form = SubmitTalkForm()
    conf = Conf.query.filter(Conf.year == year).first()
    today = date.today()
    context.update(locals())
    return render_template('conftheme/{}/parts/cfp.html'.format(year), **context)


@module_blueprint.route("/<int:year>/profile/")
@login_required
def profile(year):
    context = mhelp.context()
    userprofile_form = UserProfileForm(obj=current_user)
    author_talks_list: list = db.session.query(talk_list_author_bridge).filter(
        talk_list_author_bridge.c.user_id == current_user.id
    ).all()

    submitted_talks: list = []
    for author_talk in author_talks_list:
        talk = Talk.query.get(author_talk[1])
        submitted_talks.append(talk)

    submitted_talks = [t for t in submitted_talks if t.talk_conference.year == year]
    checked_tab = 'submited_talks'
    context.update(locals())

    return render_template('conftheme/{}/parts/profile.html'.format(year), **context)


@module_blueprint.route("/<int:year>/profile/talk/<talk_id>")
@login_required
def talk_actions(year, talk_id):
    context = mhelp.context()
    talk = Talk.query.get(talk_id)
    SubmitTalkForm_ = SubmitTalkForm
    context.update(locals())
    return render_template('conftheme/{}/parts/talk_actions.html'.format(year), **context)


def get_talk(talks, i):
    if i < 0:
        return None

    try:
        talk = talks[i]
        return i
    except IndexError:
        return None


@module_blueprint.route("/<int:year>/review/")
@module_blueprint.route("/<int:year>/review/<int:talk_num_>")
@login_required
def review(year, talk_num_=1):
    conf = Conf.query.filter(
        Conf.year == year
    ).first_or_404()
    context = mhelp.context()
    talks = conf.talks
    if talks:
        talk_num = talk_num_ - 1
        len_ = len
        next_talk = get_talk(talks, talk_num + 1)
        prev_talk = get_talk(talks, talk_num - 1)

        current_score = 0
        talk = talks[talk_num]
        for sl in talk.score_lists:
            if sl.reviewer == current_user:
                current_score = sl.score
                break
        context.update(locals())
    return render_template('conftheme/{}/parts/review.html'.format(year), **context)


@module_blueprint.route("/<int:year>/leaderboard/")
@login_required
def leaderboard(year):
    context = mhelp.context()
    conf = Conf.query.filter(
        Conf.year == year
    ).first_or_404()
    talks = [[talk, talk.get_score()] for talk in conf.talks]
    talks = sorted(talks, key=lambda l: l[1], reverse=True)
    str_ = str
    context.update(locals())
    return render_template('conftheme/{}/parts/leaderboard.html'.format(year), **context)


@module_blueprint.route("/<int:year>/schedule/")
def schedule(year):
    context = mhelp.context()
    print(context)
    timezone = request.args.get("tz", "UTC")
    DayForm_ = DayForm
    conf = Conf.query.filter(
        Conf.year == year
    ).first_or_404()

    if conf is not None and conf.schedule is None:
        conf.schedule = Schedule()

    weekmap = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    schedule = conf.schedule
    NormalActivityForm_ = NormalActivityForm
    TalkActivityForm_ = TalkActivityForm

    if not current_user.is_admin:
        context.update(locals())
        return render_template('conftheme/{}/parts/schedule_2.html'.format(year), **context)
    context.update(locals())
    return render_template('conftheme/{}/parts/schedule.html'.format(year), **context)


@module_blueprint.route("/<int:year>/schedule/activity_<int:act_id>")
def schedule_activity(year, act_id):
    context = mhelp.context()
    timezone = request.args.get("tz", "UTC")
    act_id = act_id
    activity = Activity.query.get(act_id)
    day = Day.query.get(activity.day_id)
    context.update(locals())
    return render_template('conftheme/{}/parts/activity.html'.format(year), **context)


@module_blueprint.route("/<int:year>/reviewers/")
def reviewers(year):
    context = mhelp.context()
    conf = Conf.query.filter(Conf.year == year).first_or_404()
    reviewers = None
    if conf.reviewer_list:
        reviewers = conf.reviewer_list.reviewers

    if reviewers is None:
        reviewers = []
    context.update({
        'reviewers': reviewers
    })
    return render_template('conftheme/{}/parts/reviewers.html'.format(year), **context)


@module_blueprint.route("/<int:year>/code-of-conduct/")
def coc(year):
    context = mhelp.context()
    return render_template('conftheme/{}/parts/code_of_conduct.html'.format(year), **context)


@module_blueprint.route("/<int:year>/privacy-policy/")
def privacy_policy(year):
    context = mhelp.context()
    return render_template('conftheme/{}/parts/privacy_policy.html'.format(year), **context)


@module_blueprint.route("/<int:year>/setup/")
def setup(year):
    context = mhelp.context()
    return render_template('conftheme/{}/parts/setup.html'.format(year), **context)

# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
