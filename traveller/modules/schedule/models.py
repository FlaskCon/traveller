from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from init import db
from shopyo.api.models import PkModel


class Schedule(PkModel):
    __tablename__ = "schedules"
    days = db.relationship("Day", backref=db.backref("day_schedule", lazy=True))

    conf_id = db.Column(db.Integer, db.ForeignKey("conferences.id"), nullable=False)


class Day(PkModel):
    __tablename__ = "days"

    date = db.Column(db.Date, nullable=False)
    activities = db.relationship(
        "Activity",
        backref=db.backref("activity_day", lazy=True),
        cascade="save-update, delete",
    )

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)

    def get_sorted_activities(self):
        acts = [[act, act.start_time] for act in self.activities]
        return sorted(acts, key=lambda l: l[1], reverse=True)

    def get_sorted_activities_based_on_timezone(
        self, timezoneinfo: str = "Europe/Stockholm"
    ):
        acts = []
        for act in self.activities:
            end_datetime = datetime.fromisoformat(f"{self.date} {act.end_time}")
            start_datetime = datetime.fromisoformat(f"{self.date} {act.start_time}")

            start_civil_time = datetime(
                start_datetime.year,
                start_datetime.month,
                start_datetime.day,
                start_datetime.hour,
                start_datetime.minute,
                tzinfo=ZoneInfo("Europe/Stockholm"),
            )
            end_civil_time = datetime(
                end_datetime.year,
                end_datetime.month,
                end_datetime.day,
                end_datetime.hour,
                end_datetime.minute,
                tzinfo=ZoneInfo("Europe/Stockholm"),
            )

            if timezoneinfo != "Europe/Stockholm":
                try:
                    start_civil_time = start_civil_time.astimezone(
                        tz=ZoneInfo(timezoneinfo)
                    )
                    end_civil_time = end_civil_time.astimezone(tz=ZoneInfo(timezoneinfo))
                except (ValueError, ZoneInfoNotFoundError):
                    pass

            activity_time_diff = end_civil_time - start_civil_time
            duration = self.sec_to_time_format(total_secs=activity_time_diff.seconds)
            acts.append([act, start_civil_time, duration])
        return sorted(acts, key=lambda l: l[1], reverse=False)

    def sec_to_time_format(self, total_secs=0):
        # Convert seconds to hours and minutes
        # Separate seconds into hours, and minutes
        total_secs = total_secs
        hours = (total_secs % 86400) // 3600
        total_secs %= 3600
        minutes = (total_secs % 86400) // 60
        total_secs %= 60
        return f"{hours}h{minutes}min" if hours >= 1 else f"{minutes}min"



class Activity(PkModel):
    __tablename__ = "activities"

    type = db.Column(db.String(300))
    text = db.Column(db.String(300), info={"label": "Text:"})
    start_time = db.Column(db.Time, info={"label": "Start time:"}, nullable=False)
    end_time = db.Column(db.Time, info={"label": "End time:"}, nullable=False)
    talk_id = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey("days.id"), nullable=False)

    def get_talk(self):
        from modules.conf.models import Talk

        return Talk.query.get(self.talk_id)
