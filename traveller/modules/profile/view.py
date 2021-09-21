
from shopyo.api.module import ModuleHelp
from flask_login import login_required
from flask_login import current_user
from .forms import UserProfileForm
#from sqlalchemy import func
from modules.box__default.auth.models import User
# from flask import render_template
# from flask import url_for
# from flask import redirect
from flask import render_template
#from flask import flash
#from shopyo.api.html import notify_warning
# from flask import request

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


@module_blueprint.route("/<int:year>/profile/edit", methods=['POST'])
@login_required
def edit_profile(year):
    userprofile_form = UserProfileForm(obj=current_user)
    checked_tab = 'personal_info'
    context = {}
    if userprofile_form.validate():
        userprofile_form.populate_obj(current_user)
        current_user.update()
        context.update(locals())
        return render_template('conftheme/{}/parts/profile.html'.format(year), **context)
    context.update(locals())
    return redirect(url_for('y.profile', year=year))
    
      
      
#     talk = Talk.query.get(talk_id)
#     form = SubmitTalkForm(obj=talk)
#     form.populate_obj(talk)
#     form.validate()
#     talk.update()
    
# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
