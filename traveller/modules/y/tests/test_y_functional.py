import pytest

from modules.conf.models import AuthorList


@pytest.fixture(scope="module", autouse=True)
def provide_conf_data(db, non_admin_user, conf, last_conf, talk, last_talk, schedule):
    print(non_admin_user)
    conf.reviewer_list.reviewers.append(non_admin_user)
    db.session.add(conf)
    db.session.add(last_conf)

    talk.create_slug()
    talk.author_list = AuthorList()
    talk.author_list.authors.append(non_admin_user)
    talk.submitter_id = non_admin_user.id
    talk.talk_conference = conf
    db.session.add(talk)

    last_talk.create_slug()
    last_talk.author_list = AuthorList()
    last_talk.author_list.authors.append(non_admin_user)
    last_talk.submitter_id = non_admin_user.id
    last_talk.talk_conference = last_conf
    db.session.add(last_talk)

    db.session.add(schedule)
    db.session.commit()


def test_view_landing_page__invalid_year(test_client, current_year):
    res = test_client.get(f"/y/{current_year + 5}", follow_redirects=True)
    assert res.status_code == 404


def test_view_landing_page(test_client, current_year):
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
    res = test_client.get(f"/y/{current_year}/cfp", follow_redirects=True)
    assert res.status_code == 200
    assert b"Submit a new talk" in res.data


def test_view_profile_page(test_client, login_non_admin_user, current_year, non_admin_user):
    res = test_client.get(f"/y/{current_year}/profile", follow_redirects=True)
    assert res.status_code == 200
    assert f"{non_admin_user.email}".encode("ascii") in res.data
    assert f"{non_admin_user.first_name}".encode("ascii") in res.data
    assert f"{non_admin_user.last_name}".encode("ascii") in res.data
    assert b"Test Talk" in res.data
    assert b"Test Talk2" not in res.data


def test_view_review_page(test_client, login_non_admin_user, current_year):
    res = test_client.get(f"/y/{current_year}/review", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data
    res = test_client.get(f"/y/{current_year}/review/1", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data


def test_view_leaderboard_page(test_client, login_non_admin_user, current_year):
    res = test_client.get(f"/y/{current_year}/leaderboard", follow_redirects=True)
    assert res.status_code == 200
    assert b"Test Talk" in res.data


def test_view_schedule_page(test_client, login_non_admin_user, current_year):
    res = test_client.get(f"/y/{current_year}/schedule", follow_redirects=True)
    assert res.status_code == 200
    assert b"Schedule" in res.data
    assert b"Fun and Games" in res.data


def test_view_reviewers_page(test_client, login_non_admin_user, current_year):
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
