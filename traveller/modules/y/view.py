from datetime import date
from shopyo.api.module import ModuleHelp
from flask import render_template
from modules.box__default.auth.models import User
from modules.conf.models import Conf
from modules.conf.models import Talk
from modules.schedule.forms import DayForm
from modules.cfp.forms import SubmitTalkForm
from modules.schedule.models import Schedule
from modules.schedule.forms import NormalActivityForm
from modules.schedule.forms import TalkActivityForm
from modules.profile.forms import UserProfileForm
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

from flask_login import current_user
from flask_login import login_required


# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


@module_blueprint.route("/<int:year>/")
def landing_page(year):
    context = mhelp.context()
    conf = Conf.query.filter(Conf.year==year).first_or_404()
    reviewers = conf.reviewer_list.reviewers if conf.reviewer_list is not None else None
    if reviewers is None:
        reviewers = []
    today = date.today()
    context.update(locals())
    return render_template('conftheme/{}/index.html'.format(year), **context)


@module_blueprint.route("/<int:year>/cfp/")
@login_required
def cfp(year):
    context = mhelp.context()
    talk_form = SubmitTalkForm()
    conf = Conf.query.filter(Conf.year==year).first()
    today = date.today()
    context.update(locals())
    return render_template('conftheme/{}/parts/cfp.html'.format(year), **context)


@module_blueprint.route("/<int:year>/profile/")
@login_required
def profile(year):
    context = mhelp.context()
    userprofile_form = UserProfileForm(obj=current_user)
    submitted_talks = Talk.query.filter(
        Talk.submitter_id == current_user.id
        ).all()
    submitted_talks = [t for t in submitted_talks if t.talk_conference.year == year]
    checked_tab = 'submited_talks'
    context.update(locals())
    return render_template('conftheme/{}/parts/profile.html'.format(year), **context)



@module_blueprint.route("/<int:year>/profile/talk/<talk_id>")
@login_required
def talk_actions(year, talk_id):
    context = mhelp.context()
    talk = Talk.query.get(talk_id)
    if (not int(current_user.id) == int(talk.submitter_id)):
        return '---'
    SubmitTalkForm_ = SubmitTalkForm
    context.update(locals())
    return render_template('conftheme/{}/parts/talk_actions.html'.format(year), **context)


def get_talk(talks, i):
    try:
        t = talks[i]
        if i < 0:
            return None
        return i
    except Exception as e:
        return None


@module_blueprint.route("/<int:year>/review/")
@module_blueprint.route("/<int:year>/review/<int:talk_num_>")
@login_required
def review(year, talk_num_=1):
    conf = Conf.query.filter(
            Conf.year==year
            ).first_or_404()
    context = mhelp.context()
    talks = conf.talks
    if talks:
        talk_num = talk_num_ - 1
        
        
        
        len_ = len
        next_talk = get_talk(talks, talk_num+1)
        prev_talk = get_talk(talks, talk_num-1)
        
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
        Conf.year==year
        ).first_or_404()
    talks = [[talk, talk.get_score()] for talk in conf.talks]
    talks = sorted(talks, key=lambda l:l[1], reverse=True)
    str_ = str
    context.update(locals())
    return render_template('conftheme/{}/parts/leaderboard.html'.format(year), **context)


@module_blueprint.route("/<int:year>/schedule/")
def schedule(year):
    context = mhelp.context()
    DayForm_ = DayForm
    conf = Conf.query.filter(
        Conf.year == year
        ).first_or_404()
    if conf is not None:
        if conf.schedule is None:
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
    context.update(locals())
    return render_template('conftheme/{}/parts/schedule.html'.format(year), **context)


@module_blueprint.route("/<int:year>/reviewers/")
def reviewers(year):
    context = mhelp.context()
    conf = Conf.query.filter(Conf.year==year).first_or_404()
    reviewers = conf.reviewer_list.reviewers if conf.reviewer_list is not None else None
    if reviewers is None:
        reviewers = []
    context.update({
        'reviewers': reviewers
        })
    return render_template('conftheme/{}/parts/reviewers.html'.format(year), **context)


   
# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
