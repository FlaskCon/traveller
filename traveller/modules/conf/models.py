
from init import db
from shopyo.api.models import PkModel



class Conf(PkModel):
    __tablename__ = 'conferences'
    year = db.Column(db.Integer, info={'label': 'Year'}, nullable=False)
    cfp_start = db.Column(db.Date, info={'label': 'CFP Start'}, nullable=False)
    cfp_end = db.Column(db.Date, info={'label': 'CFP End'}, nullable=False)

    talks = db.relationship('Talk',
        backref=db.backref('talk_conference', lazy=True))

    reviewer_list = db.relationship(
        "ReviewerList", backref="reviewer_list_conf", lazy=True, uselist=False
    )

    def __repr__(self):
        return 'conf:{}'.format(self.year)



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
    title = db.Column(db.String(200))
    slug = db.Column(db.String(200))
    summary = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    notes = db.Column(db.String(200))
    level = db.Column(db.String(100)) # beginner, experienced, very experienced
    accepted = db.Column(db.Boolean, default=False)

    conf_id = db.Column(db.Integer, db.ForeignKey('conferences.id'),
        nullable=False)

