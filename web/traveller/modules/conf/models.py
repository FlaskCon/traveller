import calendar
from init import db
from shopyo.api.models import PkModel

from modules.schedule.models import Schedule
from modules.box__default.auth.models import User

class Conf(PkModel):
    __tablename__ = 'conferences'
    year = db.Column(db.Integer, info={'label': 'Year'}, nullable=False)
    cfp_start = db.Column(db.Date, info={'label': 'CFP Start'}, nullable=False)
    cfp_end = db.Column(db.Date, info={'label': 'CFP End'}, nullable=False)

    talks = db.relationship('Talk',
        backref=db.backref('talk_conference', lazy=True))
    schedule = db.relationship('Schedule',
        backref=db.backref('schedule_conference', lazy=True),
        uselist=False)

    reviewer_list = db.relationship(
        "ReviewerList", backref="reviewer_list_conf", lazy=True, uselist=False
    )

    def __repr__(self):
        return 'conf:{}'.format(self.year)

    def cfp_start_repr(self):
        d = self.cfp_start
        return '{} {} {}, {}'.format(calendar.day_name[d.weekday()], d.strftime("%B"), d.day, d.year)

    def cfp_end_repr(self):
        d = self.cfp_end
        return '{} {} {}, {}'.format(calendar.day_name[d.weekday()], d.strftime("%B"), d.day, d.year)

    def add_days(self, year, cfp_start, cfp_end):
        if int(cfp_start.year) != year:
            raise ValueError("The year of the conference and the start date must be the same")
        if int(cfp_end.year) != year:
            raise ValueError("The year of the conference and the end date must be the same")
        if cfp_start > cfp_end:
            raise ValueError("The start date must be before the end date")
        self.year=year
        self.cfp_start=cfp_start
        self.cfp_end=cfp_end





conf_list_user_bridge = db.Table(
    "conf_list_user_bridge",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "reviewer_list_id",
        db.Integer,
        db.ForeignKey("reviewer_lists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ReviewerList(PkModel):

    __tablename__ = "reviewer_lists"

    conf_id = db.Column(db.Integer, db.ForeignKey("conferences.id"), nullable=False)
    reviewers = db.relationship(
        "User",
        secondary=conf_list_user_bridge,
        backref="reviewer_conf_lists",
    )


class Talk(PkModel):
    __tablename__ = 'talks'
    title = db.Column(
        db.String(200),
        nullable=False,
        info={'label': 'Title*'})
    slug = db.Column(db.String(200))
    summary = db.Column(
        db.String(300),
        nullable=False,
        info={'label': 'Summary* (max. 300 chars)'}
        )
    description = db.Column(
        db.String(3000),
        nullable=False,
        info={'label': 'Description* (max. 3000 chars)'}
        )
    notes = db.Column(
        db.String(200),
        info={'label': 'Notes (max. 200 chars)'}
        )
    level = db.Column(
        db.String(20),
        nullable=False,
        info={'label': 'Level*', 'choices': [('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced')]})
    accepted = db.Column(
        db.String(20),
        default='pending',
        info={'choices': [('accepted', 'accepted'), ('pending', 'pending'), ('rejected', 'rejected')]})

    submitter_id = db.Column(db.Integer)
    year = db.Column(db.Integer, nullable=False)
    conf_id = db.Column(db.Integer, db.ForeignKey('conferences.id'),
        nullable=False)

    author_list = db.relationship(
        "AuthorList", backref="author_list_talk", lazy=True, uselist=False, cascade='delete'
    )
    score_lists = db.relationship(
        "ScoreList", backref="score_list_talk", lazy=True, cascade='delete'
    )

    def create_slug(self):
        self.slug = self.title.replace(' ', '-')

    def get_score(self):
        score = 0
        rs = []
        for sl in self.score_lists:
            if sl.reviewer not in rs:
                score += sl.score
                rs.append(sl.reviewer)
        return score

    def __repr__(self):
        return self.title


talk_list_author_bridge = db.Table(
    "talk_list_author_bridge",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "author_list_id",
        db.Integer,
        db.ForeignKey("author_lists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class AuthorList(PkModel):

    __tablename__ = "author_lists"

    talk_id = db.Column(db.Integer, db.ForeignKey("talks.id"), nullable=False)
    authors = db.relationship(
        "User",
        secondary=talk_list_author_bridge,
        backref="author_talk_lists",
    )


talk_list_score_bridge = db.Table(
    "talk_list_score_bridge",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "score_list_id",
        db.Integer,
        db.ForeignKey("score_lists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ScoreList(PkModel):

    __tablename__ = "score_lists"

    talk_id = db.Column(db.Integer, db.ForeignKey("talks.id"), nullable=False)
    reviewer = db.relationship(
        "User",
        secondary=talk_list_score_bridge,
        backref="score_talk_lists",
        uselist=False
    )
    score = db.Column(db.Integer)
