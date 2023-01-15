"""
All initialisations like db = SQLAlchemy in this file
"""

import os
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_mailman import Mail
from flask_wtf.csrf import CSRFProtect

root_path = os.path.dirname(os.path.abspath(__file__)) # don't remove
static_path = os.path.join(root_path, "static") # don't remove
modules_path = os.path.join(root_path, "modules") # don't remove
themes_path = os.path.join(static_path, "themes") # don't remove

installed_packages = []

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
images = UploadSet("images", IMAGES, default_dest=lambda app: static_path + '/images_uploads')
tzinfo, conf_time_zone = ZoneInfo, ZoneInfo("UTC")

from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

