import click
from faker import Faker
import datetime
from modules.box__default.auth.models import User
from modules.box__default.auth.models import Role
from modules.conf.models import Conf
from modules.conf.models import Talk
from modules.conf.models import AuthorList
from init import db


SEP_CHAR = "#"
SEP_NUM = 23

faker = Faker()

talks = [
    [
        faker.sentence(nb_words=10),  # Title
        faker.text(max_nb_chars=300),  # summary
        faker.text(max_nb_chars=3000),  # description
        faker.text(max_nb_chars=200),  # notes
        ] for i in range(10)
]

reviewers = [
    [faker.first_name(), faker.last_name(), faker.email()] for i in range(10)
]


def register(app):
    @app.cli.group()
    def seed():
        """ seed the application with dev or production data """

    @seed.command()
    def dev():
        click.echo('SEEDING FOR DEV')
        click.echo('Adding Conference')
        add_conf()
        click.echo(SEP_CHAR * SEP_NUM)
        click.echo('Adding Reviews')
        add_reviewers()
        click.echo(SEP_CHAR * SEP_NUM)
        click.echo('Done.')

    @seed.command()
    def prod():
        click.echo('SEEDING FOR PROD')
        click.echo('nothing to do... yet.')


def add_conf():
    conf = Conf(
        year=2021,
        cfp_start=datetime.date(2021, 10, 1),
        cfp_end=datetime.date(2021, 10, 31)
        )
    conf.save()

    admin = User.query.get(1)
    admin.first_name = faker.first_name()
    admin.last_name = faker.last_name()
    admin.update(commit=False)

    for t in talks:
        talk = Talk()
        talk.title = t[0].strip('.')
        talk.create_slug()
        talk.summary = t[1]
        talk.description = t[2]
        talk.notes = t[3]
        talk.level = 'beginner'
        talk.duration = 1800
        talk.submitter_id = 1
        talk.author_list = AuthorList()
        talk.author_list.authors.append(admin)
        talk.conf_id = conf.id
        talk.year = 2021

        talk.save(commit=False)

    db.session.commit()


def add_reviewers():
    r1 = Role(name='reviewer', permission_level=2)
    r2 = Role(name='staff', permission_level=2)

    roles = [r1, r2]

    for r in roles:
        r.save(commit=False)

    for r in reviewers:
        user = User()
        user.first_name = r[0]
        user.last_name = r[1]
        user.email = r[2]
        user.password = 'pass'
        user.is_admin = False
        user.is_email_confirmed = True
        user.roles.append(r1)
        user.email_confirm_date = datetime.datetime.now()
        user.save(commit=False)
        user.image = "https://i.pravatar.cc/300"

    db.session.commit()
