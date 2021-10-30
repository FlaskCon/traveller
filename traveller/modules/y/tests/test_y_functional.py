import datetime

from modules.conf.models import Conf, ReviewerList, AuthorList
from modules.conf.models import Talk
from modules.schedule.models import Schedule, Day, Activity

from app import app


def create_conf(now, current_year):
    _30_days_ago = now - datetime.timedelta(days=30)
    _30_days_from_now = now + datetime.timedelta(days=30)
    return Conf.create(
        year=current_year,
        cfp_start=_30_days_ago.date(),
        cfp_end=_30_days_from_now.date(),
        reviewer_list=ReviewerList()
    )


def test_view_landing_page__invalid_year(test_client, current_year):
    res = test_client.get(f"/y/{current_year + 5}", follow_redirects=True)
    assert res.status_code == 404


def test_view_landing_page(test_client, current_year):
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    res = test_client.get(f"/y/{current_year}", follow_redirects=True)
    assert res.status_code == 200
    assert f"FLASKCON {current_year}".encode("ascii") in res.data


def test_view_about_page(test_client, current_year):
    res = test_client.get(f"/y/{current_year}/about", follow_redirects=True)
    assert res.status_code == 200
    assert b"About FlaskCon" in res.data


def test_view_contact_page(test_client, current_year):
    res = test_client.get(f"/y/{current_year}/contact", follow_redirects=True)
    assert res.status_code == 200
    assert b"Contact" in res.data
    assert b"flaskcon@gmail.com" in res.data


def test_view_cfp_page(test_client, login_non_admin_user, current_year):
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    res = test_client.get(f"/y/{current_year}/cfp", follow_redirects=True)
    assert res.status_code == 200
    assert b"Submit a new talk" in res.data


def test_view_profile_page(test_client, login_non_admin_user, current_year, non_admin_user, db_session):
    non_admin_user = db_session.merge(non_admin_user)
    now = datetime.datetime.now()
    last_year = now - datetime.timedelta(days=365)
    conf = create_conf(now, current_year)
    last_conf = create_conf(last_year, current_year - 1)
    talk = Talk.create(
        id=1,
        title="Test Talk",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=conf.year,
        conf_id=conf.id,
        submitter_id=non_admin_user.id,
        duration=1800
    )
    talk.create_slug()
    talk.author_list = AuthorList()
    talk.author_list.authors.append(non_admin_user)
    talk.update()
    old_talk = Talk.create(
        id=2,
        title="Test Talk2",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=last_year.year,
        conf_id=last_conf.id,
        submitter_id=non_admin_user.id,
        duration=1800
    )
    old_talk.create_slug()
    old_talk.author_list = AuthorList()
    old_talk.author_list.authors.append(non_admin_user)
    old_talk.update()

    res = test_client.get(f"/y/{current_year}/profile", follow_redirects=True)
    assert res.status_code == 200
    assert f"{non_admin_user.email}".encode("ascii") in res.data
    assert f"{non_admin_user.first_name}".encode("ascii") in res.data
    assert f"{non_admin_user.last_name}".encode("ascii") in res.data
    assert b"Test Talk" in res.data
    assert b"Test Talk2" not in res.data


def test_view_review_page(test_client, login_non_admin_user, current_year, non_admin_user, db_session):
    non_admin_user = db_session.merge(non_admin_user)
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    talk = Talk.create(
        id=1,
        title="Test Talk",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=conf.year,
        conf_id=conf.id,
        submitter_id=non_admin_user.id,
        duration=1800
    )
    talk.create_slug()
    talk.author_list = AuthorList()
    talk.author_list.authors.append(non_admin_user)
    talk.update()
    res = test_client.get(f"/y/{current_year}/review", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data
    res = test_client.get(f"/y/{current_year}/review/1", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data


def test_view_leaderboard_page(test_client, login_non_admin_user, current_year, non_admin_user, db_session):
    non_admin_user = db_session.merge(non_admin_user)
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    talk = Talk.create(
        id=1,
        title="Test Talk",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=conf.year,
        conf_id=conf.id,
        submitter_id=non_admin_user.id,
        duration=1800
    )
    talk.create_slug()
    talk.author_list = AuthorList()
    talk.author_list.authors.append(non_admin_user)
    talk.update()
    res = test_client.get(f"/y/{current_year}/leaderboard", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data


def test_view_schedule_page(test_client, login_non_admin_user, current_year):
    
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    Schedule.create(
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
    res = test_client.get(f"/y/{current_year}/schedule", follow_redirects=True)
    assert res.status_code == 200
    assert b"Schedule" in res.data
    assert b"Fun and Games" in res.data


def test_view_reviewers_page(test_client, login_non_admin_user, current_year, non_admin_user, db_session):
    non_admin_user = db_session.merge(non_admin_user)
    now = datetime.datetime.now()
    conf = create_conf(now, current_year)
    conf.reviewer_list.reviewers.append(non_admin_user)
    res = test_client.get(f"/y/{current_year}/reviewers", follow_redirects=True)
    assert res.status_code == 200
    assert b"Reviewers" in res.data
    assert b"TestFirst" in res.data


def test_view_code_of_conduct__page(test_client, current_year):
    res = test_client.get(f"/y/{current_year}/code-of-conduct", follow_redirects=True)
    assert res.status_code == 200
    assert b"Code of Conduct" in res.data


def test_view_privacy_policy__page(test_client, current_year):
    res = test_client.get(f"/y/{current_year}/privacy-policy", follow_redirects=True)
    assert res.status_code == 200
    assert b"Data Privacy Policy" in res.data


def test_view_setup__page(test_client, current_year):
    res = test_client.get(f"/y/{current_year}/setup", follow_redirects=True)
    assert res.status_code == 200
    assert b"Conference Setup" in res.data
