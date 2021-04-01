
from shopyo.api.module import ModuleHelp
from flask import render_template
from modules.conf.models import Conf
from modules.conf.models import Talk
from modules.cfp.forms import SubmitTalkForm
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

from flask_login import current_user

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
    return render_template('conftheme/{}/index.html'.format(year))


@module_blueprint.route("/<int:year>/cfp/")
def cfp(year):
    context = mhelp.context()
    talk_form = SubmitTalkForm()
    conf = Conf.query.filter(Conf.year==year).first()
    context.update(locals())
    return render_template('conftheme/{}/parts/cfp.html'.format(year), **context)


@module_blueprint.route("/<int:year>/profile/")
def profile(year):
    context = mhelp.context()
    submitted_talks = Talk.query.filter(
        Talk.submitter_id == current_user.id
        ).all()

    submitted_talks = [t for t in submitted_talks if t.talk_conference.year == year]
    context.update(locals())
    return render_template('conftheme/{}/parts/profile.html'.format(year), **context)



@module_blueprint.route("/<int:year>/profile/talk/<talk_id>")
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
def review(year, talk_num_=1):
    talk_num = talk_num_ - 1
    context = mhelp.context()
    conf = Conf.query.filter(
        Conf.year==year
        ).first_or_404()
    talks = conf.talks
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


# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
