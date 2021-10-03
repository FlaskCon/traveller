"""
File conftest.py contains pytest fixtures that are used in numerous
test functions. Refer to https://docs.pytest.org/en/stable/fixture.html
for more details on pytest
"""
import json
import os
import pathlib

import pytest
import datetime
from flask import url_for

from app import create_app
from init import db as _db
from modules.box__default.auth.models import User, Role
from modules.box__default.settings.models import Settings

# run in shopyo/shopyo
# python -m pytest . or python -m pytest -v
from modules.conf.models import Conf, Talk, AuthorList, ReviewerList
from modules.schedule.models import Schedule, Day, Activity

if os.path.exists("testing.db"):
    os.remove("testing.db")


@pytest.fixture(scope="session")
def unconfirmed_user():
    """
    A pytest fixture that returns a non admin user
    """
    user = User(id=1)
    user.email = "unconfirmed@domain.com"
    user.password = "pass"
    user.is_email_confirmed = False
    return user


@pytest.fixture(scope="session")
def non_admin_user():
    """
    A pytest fixture that returns a non admin user
    """
    user = User(id=2)
    user.email = "admin1@domain.com"
    user.password = "pass"
    user.first_name = "TestFirst"
    user.last_name = "TestSecond"
    user.is_email_confirmed = True
    user.email_confirm_date = datetime.datetime.now()
    return user


@pytest.fixture(scope="session")
def admin_user():
    """
    A pytest fixture that returns an admin user
    """
    user = User(id=3)
    user.email = "admin2@domain.com"
    user.password = "pass"
    user.is_admin = True
    user.is_email_confirmed = True
    user.email_confirm_date = datetime.datetime.now()
    return user


@pytest.fixture(scope="session")
def conf(current_year):
    """
    A pytest fixture that returns a conference for the current year
    """

    now = datetime.datetime.now()
    _30_days_ago = now - datetime.timedelta(days=30)
    _30_days_from_now = now + datetime.timedelta(days=30)
    conf = Conf(id=1)
    conf.year = current_year
    conf.cfp_start = _30_days_ago.date()
    conf.cfp_end = _30_days_from_now.date()
    conf.reviewer_list = ReviewerList()
    return conf


@pytest.fixture(scope="session")
def last_conf(current_year):
    """
    A pytest fixture that returns a conference for the last year
    """

    now = datetime.datetime.now()
    _30_days_ago = now - datetime.timedelta(days=365+30)
    _30_days_from_now = now - datetime.timedelta(days=365-30)
    conf = Conf()
    conf.year = current_year - 1
    conf.cfp_start = _30_days_ago.date()
    conf.cfp_end = _30_days_from_now.date()
    return conf


@pytest.fixture(scope="session")
def talk(current_year):
    return Talk(
        id=1,
        title="Test Talk",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=current_year
    )


@pytest.fixture(scope="session")
def last_talk(current_year):
    return Talk(
        id=2,
        title="Test Talk2",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=current_year - 1
    )


@pytest.fixture(scope="session")
def schedule(conf):
    return Schedule(
        days=[
            Day(
                id=1,
                date=conf.cfp_end,
                activities=[
                    Activity(
                        type="normal_activity",
                        text="Fun and Games",
                        start_time=datetime.time(9, 30),
                        end_time=datetime.time(10, 0),
                    )
                ],
            ),
        ],
        conf_id=conf.id
    )


@pytest.fixture(scope="session")
def flask_app():
    flask_app = create_app("testing")
    return flask_app


@pytest.fixture(scope="session")
def test_client(flask_app):
    """
    setups up and returns the flask testing app
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="session")
def db(test_client, non_admin_user, admin_user, unconfirmed_user, conf, last_conf, talk, last_talk, schedule):
    """
    creates and returns the initial testing database
    """
    # Create the database and the database table
    _db.app = test_client
    _db.create_all()

    # Insert admin, non admin, and unconfirmed
    _db.session.add(non_admin_user)
    _db.session.add(admin_user)
    _db.session.add(unconfirmed_user)
    conf.reviewer_list.reviewers.append(non_admin_user)
    _db.session.add(conf)
    _db.session.add(last_conf)

    talk.create_slug()
    talk.author_list = AuthorList()
    talk.author_list.authors.append(non_admin_user)
    talk.submitter_id = non_admin_user.id
    talk.talk_conference = conf
    _db.session.add(talk)

    last_talk.create_slug()
    last_talk.author_list = AuthorList()
    last_talk.author_list.authors.append(non_admin_user)
    last_talk.submitter_id = non_admin_user.id
    last_talk.talk_conference = last_conf
    _db.session.add(last_talk)

    _db.session.add(schedule)

    config_json_file = pathlib.Path(__file__).parent.resolve().joinpath("config.json")
    # add the default settings
    with open(config_json_file, "r") as config:
        config = json.load(config)
    for name, value in config["settings"].items():
        s = Settings(setting=name, value=value)
        _db.session.add(s)

    # Commit the changes for the users
    _db.session.commit()

    yield _db  # this is where the testing happens!

    _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def db_session(db):
    """
    Creates a new database session for a test. Note you must use this fixture
    if your test connects to db. Autouse is set to true which implies
    that the fixture will be setup before each test

    Here we not only support commit calls but also rollback calls in tests.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope="session")
def current_year():
    return datetime.datetime.now().year


@pytest.fixture
def login_unconfirmed_user(auth, unconfirmed_user):
    """Login with unconfirmed and logout during teadown"""
    auth.login(unconfirmed_user)
    yield
    auth.logout()


@pytest.fixture
def login_admin_user(auth, admin_user):
    """Login with admin and logout during teadown"""
    auth.login(admin_user)
    yield
    auth.logout()


@pytest.fixture
def login_non_admin_user(auth, non_admin_user):
    """Login with non-admin and logout during teadown"""
    auth.login(non_admin_user)
    yield
    auth.logout()


@pytest.fixture
def auth(test_client):
    return AuthActions(test_client)


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, user, password="pass"):
        return self._client.post(
            url_for("auth.login"),
            data=dict(email=user.email, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self._client.get(url_for("auth.logout"), follow_redirects=True)


# Want TO USE THE BELOW 2 FIXTURES TO DYNAMICALLY
# GET THE ROUTES FOR A GIVEN MODULE BUT UNABLE TO
# PARAMETERIZE THE LIST OF ROUTES RETURNED FROM THE FIXTURE
# CURRENTLY THIS NOT POSSIBLE WITH FIXTURES IN PYTEST @rehmanis

# @pytest.fixture(scope="module")
# def get_module_routes(request, get_routes):
#     module_prefix = getattr(request.module, "module_prefix", "/")
#     return get_routes[module_prefix]


# @pytest.fixture(scope="session")
# def get_routes(flask_app):

#     routes_dict = {}
#     relative_path = "/"
#     prefix = "/"

#     for route in flask_app.url_map.iter_rules():
#         split_route = list(filter(None, str(route).split("/", 2)))

#         if len(split_route) == 0:
#             prefix = "/"
#             relative_path = ""
#         elif len(split_route) == 1:
#             prefix = "/" + split_route[0]
#             relative_path = "/"
#         else:
#             prefix = "/" + split_route[0]
#             relative_path = split_route[1]

#         if prefix in routes_dict:
#             routes_dict[prefix].append(relative_path)
#         else:
#             routes_dict[prefix] = [relative_path]

#     return routes_dict
