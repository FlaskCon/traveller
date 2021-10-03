import datetime

import pytest

from modules.conf.models import Talk, ReviewerList, Conf
from modules.schedule.models import Schedule, Day, Activity


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def talk(current_year):
    return Talk(
        id=1,
        title="Test Talk",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=current_year
    )


@pytest.fixture(scope="module")
def last_talk(current_year):
    return Talk(
        id=2,
        title="Test Talk2",
        summary="Some summary",
        description="Some Description",
        level="beginner",
        year=current_year - 1
    )


@pytest.fixture(scope="module")
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