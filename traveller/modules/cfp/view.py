'''
Manages CFP. Adds talk to conferences
Lets reviewers review talks
'''
from shopyo.api.module import ModuleHelp
from modules.box__default.auth.models import User
from modules.conf.models import Conf
from modules.conf.models import Talk
from modules.conf.models import AuthorList
from modules.conf.models import ScoreList
from modules.cfp.forms import SubmitTalkForm
from modules.cfp.forms import AdminTalkForm
from flask import render_template
# from flask import url_for
# from flask import redirect
from flask import flash
from flask import request
from flask_login import login_required
from flask_login import current_user

from helpers.c2021.notif import alert_success, alert_danger

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


@module_blueprint.route("/<year>/talk", methods=['POST'])
@login_required
def add_talk(year):
    form = SubmitTalkForm()

    if not form.validate():
        alert_danger('Talk not submitted!')
        return mhelp.redirect_url('y.cfp', year=year)

    conf = Conf.query.filter(
        Conf.year==year
        ).first_or_404()
    talk = Talk()
    form.populate_obj(talk)
    talk.create_slug()
    if talk.author_list is None:
        talk.author_list = AuthorList()
        
    talk.author_list.authors.append(current_user)
    talk.submitter_id = current_user.id
    talk.year = year
    talk.talk_conference = conf

    co_authors_email: str = request.form.get('co_authors')
    co_authors_email_list:list = co_authors_email.split('\n') if len(co_authors_email) != 0 else []
    for author_email in co_authors_email_list:
        user = User.query.filter(User.email==author_email).first()
        if user not in talk.author_list.authors:
            talk.author_list.authors.append(user)

    conf.talks.append(talk)
    conf.update()
    alert_success('Talk submitted!')
    return mhelp.redirect_url('y.cfp', year=year)


@module_blueprint.route("/<year>/talk/<talk_id>", methods=['POST'])
@login_required
def edit_talk(year, talk_id):
    talk = Talk.query.get(talk_id)
    form = SubmitTalkForm(obj=talk)
    form.populate_obj(talk)
    form.validate()

    co_authors_email_list: list = request.form.getlist('co_authors')
    for author_email in co_authors_email_list:
        user = User.query.filter(User.email==author_email).first()
        if user not in talk.author_list.authors:
            talk.author_list.authors.append(user)

    for author in talk.author_list.authors:
        if author.email not in co_authors_email_list \
            and author.id != talk.submitter_id:
            talk.author_list.authors.remove(author)

    talk.update()
    return mhelp.redirect_url('y.talk_actions', year=year, talk_id=talk_id)


@module_blueprint.route("/<year>/talk/<talk_id>/rate/<int:score>/<talk_num_>")
@login_required
def rate_talk(year, talk_id, score, talk_num_):
    if score not in [0, 1, 2]:
        return '---'
    talk = Talk.query.get(talk_id)
    reviewers = [sl.reviewer for sl in talk.score_lists]
    if current_user not in reviewers:
        
        score_list = ScoreList()
        score_list.score = score
        score_list.reviewer = current_user
        score_list.talk_id = talk.id
        talk.score_lists.append(score_list)
        talk.update()
    else:
        for sl in talk.score_lists:
            if sl.reviewer == current_user:
                sl.score = score
                sl.update()
                break
    return mhelp.redirect_url('y.review', year=year, talk_num_=talk_num_)


@module_blueprint.route("/<year>/talk/<talk_id>/final_talk_action", methods=["GET", "POST"])
@login_required
def final_talk_action(year, talk_id):
    if request.method == 'GET':
        context = mhelp.context()
        talk = Talk.query.get(talk_id)
        AdminTalkForm_ = AdminTalkForm

        context.update(locals())
        return render_template('conftheme/{}/parts/final_talk_action.html'.format(year), **context)
    elif request.method == 'POST':
        talk = Talk.query.get(talk_id)
        form = AdminTalkForm(obj=talk)
        form.populate_obj(talk)
        form.validate()

        talk.update()
        alert_success('Talk status changed!')
        return mhelp.redirect_url('cfp.final_talk_action', year=year, talk_id=talk_id)



@module_blueprint.route("/<year>/talk/<talk_id>/delete")
@login_required
def delete_talk(year, talk_id):
    talk = Talk.query.get(talk_id)
    talk.delete()    
    return mhelp.redirect_url('y.profile', year=year)
