import importlib
import os
import json
import jinja2

from flask import Flask
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from flask_admin import Admin
from shopyo_admin import DefaultModelView
from shopyo_admin import MyAdminIndexView
from flask_admin.menu import MenuLink
from flask_uploads import configure_uploads
from jinja2.filters import pass_eval_context

from modules.box__default.settings.helpers import get_setting
from modules.box__default.settings.models import Settings
from config import app_config

from init import db
from init import login_manager
from init import ma
from init import migrate
from init import mail
from init import modules_path
from init import images
from init import csrf

from shopyo.api.file import trycopy
import seed

from side_load_2023 import side_load_2023

#
# secrets files
#


try:
    if not os.path.exists("config.json"):
        trycopy("config_demo.json", "config.json")
except PermissionError as e:
    print(
        "Cannot continue, permission error"
        "initializing config.py and config.json, "
        "copy and rename them yourself!"
    )
    raise e

base_path = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name="development"):
    global_template_variables = {}
    global_configs = {}
    app = Flask(
        __name__,
        instance_path=os.path.join(base_path, "instance"),
        instance_relative_config=True,
    )
    load_config_from_obj(app, config_name)
    load_config_from_instance(app, config_name)
    create_config_json()
    load_extensions(app)
    setup_flask_admin(app)
    register_devstatic(app)
    load_blueprints(app, config_name, global_template_variables, global_configs)
    setup_theme_paths(app)
    inject_global_vars(app, global_template_variables)

    side_load_2023(app)

    return app


def load_config_from_obj(app, config_name):
    try:
        configuration = app_config[config_name]
    except KeyError as e:
        print(
            f"[ ] Invalid config name {e}. Available configurations are: "
            f"{list(app_config.keys())}\n"
        )
        sys.exit(1)

    app.config.from_object(configuration)


def load_config_from_instance(app, config_name):
    if config_name != "testing":
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    # create empty instance folder and empty config if not present
    try:
        os.makedirs(app.instance_path)
        with open(os.path.join(app.instance_path, "config.py"), "a"):
            pass
    except OSError:
        pass


def create_config_json():
    if not os.path.exists("config.json"):
        trycopy("config_demo.json", "config.json")


def load_extensions(app):
    migrate.init_app(app, db)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    seed.register(app)
    csrf.init_app(app)
    configure_uploads(app, images)


def setup_flask_admin(app):
    admin = Admin(
        app,
        name="My App",
        template_mode="bootstrap4",
        index_view=MyAdminIndexView(),
    )
    # admin.add_view(DefaultModelView(Settings, db.session))
    admin.add_view(DefaultModelView(Settings, db.session))
    admin.add_link(MenuLink(name="Logout", category="", url="/auth/logout?next=/admin"))


def register_devstatic(app):
    @app.route("/devstatic/<path:boxormodule>/f/<path:filename>")
    def devstatic(boxormodule, filename):
        if app.config["DEBUG"]:
            module_static = os.path.join(modules_path, boxormodule, "static")
            return send_from_directory(module_static, filename=filename)


def load_blueprints(app, config_name, global_template_variables, global_configs):
    """
    - Registers blueprints
    - Adds global template objects from modules
    - Adds global configs from modules
    """

    for folder in os.listdir(os.path.join(base_path, "modules")):
        if folder.startswith("__"):  # ignore __pycache__
            continue

        if folder.startswith("box__"):
            # boxes
            for sub_folder in os.listdir(os.path.join(base_path, "modules", folder)):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                try:
                    sys_mod = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.view"
                    )
                    app.register_blueprint(getattr(sys_mod, f"{sub_folder}_blueprint"))
                except AttributeError:
                    pass
                try:
                    mod_global = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.global"
                    )
                    global_template_variables.update(mod_global.available_everywhere)
                except ImportError:
                    pass

                except AttributeError:
                    pass

                # load configs
                try:
                    mod_global = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.global"
                    )
                    if config_name in mod_global.configs:
                        global_configs.update(mod_global.configs.get(config_name))
                except ImportError:
                    pass

                except AttributeError:
                    # click.echo('info: config not found in global')
                    pass
        else:
            # apps
            try:
                mod = importlib.import_module(f"modules.{folder}.view")
                app.register_blueprint(getattr(mod, f"{folder}_blueprint"))
            except AttributeError:
                # print("[ ] Blueprint skipped:", e)
                pass

            # global's available everywhere template vars
            try:
                mod_global = importlib.import_module(f"modules.{folder}.global")
                global_template_variables.update(mod_global.available_everywhere)
            except ImportError:
                # print(f"[ ] {e}")
                pass

            except AttributeError:
                pass

            # load configs
            try:
                mod_global = importlib.import_module(f"modules.{folder}.global")
                if config_name in mod_global.configs:
                    global_configs.update(mod_global.configs.get(config_name))
            except ImportError:
                # print(f"[ ] {e}")
                pass
            except AttributeError:
                # click.echo('info: config not found in global')
                pass

    app.config.update(**global_configs)


def setup_theme_paths(app):
    with app.app_context():
        front_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "front"
        )
        back_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "back"
        )
        my_loader = jinja2.ChoiceLoader(
            [
                app.jinja_loader,
                jinja2.FileSystemLoader([front_theme_dir, back_theme_dir]),
            ]
        )
        app.jinja_loader = my_loader


def inject_global_vars(app, global_template_variables):
    @app.context_processor
    def inject_global_vars():
        APP_NAME = "dwdwefw"

        base_context = {
            "APP_NAME": APP_NAME,
            "len": len,
            "current_user": current_user,
        }
        base_context.update(global_template_variables)

        return base_context

    @app.template_filter()
    @pass_eval_context
    def get_enum(eval_ctx, value):
        # Custom filter to return enumerated iterable
        return enumerate(value)
