
from shopyo.api.module import ModuleHelp
from modules.conf.forms import ConfForm
from modules.conf.models import Conf
from modules.conf.models import ReviewerList
from modules.box__default.auth.models import User
from modules.box__default.auth.models import Role
# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
from flask import request

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']

def get_reviewers():
    reviewers = []
    for user in User.query.all():
        if 'reviewer' in [r.name for r in user.roles]:
            reviewers.append(user)
    return reviewers

@module_blueprint.route("/dashboard", methods=["GET"])
def dashboard():

    context = mhelp.context()
    conf_form = ConfForm()
    ConfForm_ = ConfForm
    confs = Conf.query.all()
    reviewers = get_reviewers()

    context.update(locals())
    return mhelp.render('dashboard.html', **context)


@module_blueprint.route("/add", methods=["POST"])
def add():
    form = ConfForm()
    form.validate()
    conf = Conf()
    conf.year = form.year.data
    conf.cfp_start = form.cfp_start.data
    conf.cfp_end = form.cfp_end.data
    conf.save()
    return mhelp.redirect_url('conf.dashboard')

@module_blueprint.route("/<conf_id>/edit", methods=["POST"])
def edit(conf_id):
    form = ConfForm()
    conf = Conf.query.get(conf_id)
    form = ConfForm(obj=conf)
    form.populate_obj(conf)
    form.validate()

    conf.year = form.year.data
    conf.cfp_start = form.cfp_start.data
    conf.cfp_end = form.cfp_end.data
    conf.update()
    return mhelp.redirect_url('conf.dashboard')


@module_blueprint.route("/<conf_id>/delete", methods=["POST"])
def delete(conf_id):
    conf = Conf.query.get(conf_id)
    conf.delete()
    return mhelp.redirect_url('conf.dashboard')


@module_blueprint.route("/<conf_id>/reviewers/update", methods=["POST"])
def update_reviewers(conf_id):
    conf = Conf.query.get(conf_id)
    if conf.reviewer_list is None:
        conf.reviewer_list = ReviewerList()
    conf.reviewer_list.reviewers = []
    for elem in request.form:
        if elem.startswith('reviewer'):
            r_id = elem.split('_')[1]
            r = User.query.get(r_id)
            conf.reviewer_list.reviewers.append(r)
    conf.update()
    return mhelp.redirect_url('conf.dashboard')