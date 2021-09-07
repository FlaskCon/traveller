from init import db
from shopyo.api.models import PkModel



class Schedule(PkModel):
    __tablename__ = 'schedules'
    days = db.relationship('Day',
        backref=db.backref('day_schedule', lazy=True))
    
    conf_id = db.Column(db.Integer, db.ForeignKey("conferences.id"), nullable=False)


class Day(PkModel):
    __tablename__ = 'days'
    
    date = db.Column(db.Date, nullable=False)
    activities = db.relationship('Activity',
        backref=db.backref('activity_day', lazy=True))

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)

    def get_sorted_activities(self):
        acts = [[act, act.start_time] for act in self.activities]
        return sorted(acts,key=lambda l:l[1], reverse=True)


class Activity(PkModel):
    __tablename__ = 'activities'
    

    type = db.Column(db.String(300))
    text = db.Column(db.String(300))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    talk_id = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey("days.id"), nullable=False)

    def get_talk(self):
        from modules.conf.models import Talk
        return Talk.query.get(self.talk_id)