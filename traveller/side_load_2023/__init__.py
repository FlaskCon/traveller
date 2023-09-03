from flask import Flask


def side_load_2023(app: Flask):
    from flask import Blueprint

    bp = Blueprint(
        'side_load_2023',
        __name__,
        template_folder='static/themes/front/conftheme',
        url_prefix='/y/2023/event-schedule'
    )

    @bp.route('/')
    def index():
        return 'Hello World!'

    app.register_blueprint(bp)
