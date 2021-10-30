from datetime import datetime
try:
    from zoneinfo import ZoneInfoNotFoundError
except ImportError:
    from backports.zoneinfo import ZoneInfoNotFoundError
    
from init import db, conf_time_zone, tzinfo
from shopyo.api.models import PkModel


class Schedule(PkModel):
    __tablename__ = "schedules"
    days = db.relationship("Day", backref=db.backref("day_schedule", lazy=True))

    conf_id = db.Column(db.Integer, db.ForeignKey("conferences.id"), nullable=False)


class Day(PkModel):
    __tablename__ = "days"

    date = db.Column(db.Date, nullable=False, unique=True, info={"label": "Date:"})
    activities = db.relationship(
        "Activity",
        backref=db.backref("activity_day", lazy=True),
        cascade="save-update, delete",
    )

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)


    def get_sorted_activities_based_on_timezone(self, timezoneinfo: str) -> list:
        """
        get_sorted_activities_based_on_timezone Method that sorts the daily activities using the start time.

        The method does the following:
          - formats both the start and end times of an activity using the timezone information provided:
          - finds the duration for a normal activity
          - appends to a list containing activities, their start time, and duration
          - sorts the list in ascending order using the start time

        :param timezoneinfo: a timezone from the IANA timezone list
        :type timezoneinfo: str
        :return: a sorted list containing activities, their start time, and duration
        :rtype: list
        """
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
                tzinfo=conf_time_zone,
            )
            end_civil_time = datetime(
                end_datetime.year,
                end_datetime.month,
                end_datetime.day,
                end_datetime.hour,
                end_datetime.minute,
                tzinfo=conf_time_zone,
            )

            if timezoneinfo != "UTC":
                try:
                    start_civil_time = start_civil_time.astimezone(
                        tz=tzinfo(timezoneinfo)
                    )
                    end_civil_time = end_civil_time.astimezone(tz=tzinfo(timezoneinfo))
                except (ValueError, ZoneInfoNotFoundError):
                    pass

            activity_time_diff = end_civil_time - start_civil_time
            duration = self.sec_to_time_format(total_secs=activity_time_diff.seconds)
            if act.type == 'talk':
                talk = act.get_talk()
                duration = self.sec_to_time_format(total_secs=talk.duration)
            acts.append([act, start_civil_time, duration])
        return sorted(acts, key=lambda l: l[1], reverse=False)

    def get_time_indicators(self, timezoneinfo: str, year: int):
        """
        get_time_indicators Method that provides the time inidicators used for the frontend.

        This method works by first setting the default start date and time of the conference to 1/12/conf_year 09:00:00+UTC.
        The start date and time is then converted into the timezone information provided.
        
        We then generate a list of time indicators in the given timezone.
        We create a dictionary with the elements in the list of time indicators as key and 
        a list containing 2 elements as the value.


        :param timezoneinfo: a timezone from the IANA timezone list
        :type timezoneinfo: str
        :param year: the conference year
        :type year: int
        :return: a tuple containing a list of time indicators and a dictionary with time intervals.
        :rtype: tuple
        """
        start_time = datetime(year, 12, 1, 9, 0, tzinfo=conf_time_zone)
        try:
            converted_start_time = start_time.astimezone(tz=tzinfo(timezoneinfo))
        except (ValueError, ZoneInfoNotFoundError):
            converted_start_time = start_time.astimezone(tz=conf_time_zone)

        indicators = []
        number_of_hour_intervals = 9    # Initialised as 9 b'cus number of 1 hour intervals between 9:00:00 to 18:00:00 is 9.
        for item in range(0, number_of_hour_intervals):
            # The purpose of this loop is to determine the list of time indicators to use when the timezone changes.
            # For example; if the timezone is set to Australia/Queensland which has a UTC offset of +10:00, then the start time
            # changes from 9:00:00+UTC to 19:00:00+Australia/Queensland and we could calculate the remaining time indicators.
            
            # We loop through a range from 0 to number_of_hour_intervals. We used 9 as the stop for the range 
            # because the number of 1 hour intervals between 9:00:00 to 18:00:00 is 9.

            cc = converted_start_time
            c_hour = int(cc.hour + item)
            if c_hour > 23:
                # if c_hour > 23 then we subtract 24 it which leaves us with a remainder < 23. 
                # The remainder represents an hour for the next day
                c_hour-=24
            cc = cc.replace(hour=c_hour)
            indicators.append(cc)
            cc = cc.replace(minute=30)
            indicators.append(cc)

        hh = converted_start_time
        h_hour = int(hh.hour + number_of_hour_intervals)
        if h_hour > 23:
                h_hour-=24
        hh = hh.replace(hour=h_hour)
        indicators.append(hh)

        pair_indicators = {}
        prev = indicators[0]
        for j in range(0, len(indicators)):
            # The purpose of this loop is to determine the time range that an activity falls under.
            # We achieve the purpose by creating a dictionary which has a time indicator as the the key and
            # a list of time indicators (current time indicator and next time indicator) as the value
            # For example; if time indicator is 9:00:00 then 
            # the elements in the dictionary will be {"9:00:00": [9:00:00, 9:30:00]}

            try:
                next_ = indicators[int(j + 1)]
                pair_indicators.update([(f"{prev}",[prev, next_])])
                prev = next_
            except IndexError:
                next_ = indicators[0]
                pair_indicators.update(([(f"{prev}",[prev, next_])]))
                prev = prev
        return indicators, pair_indicators

    def sec_to_time_format(self, total_secs=0):
        # Convert seconds to hours and minutes
        # Separate seconds into hours, and minutes
        total_secs = total_secs
        hours = (total_secs % 86400) // 3600
        total_secs %= 3600
        minutes = (total_secs % 86400) // 60
        total_secs %= 60
        if hours >= 1 and minutes > 0:
            duration = f"{hours}h{minutes}m"
        elif hours >= 1 and minutes <= 0:
            duration = f"{hours}hr"
        else: duration = f"{minutes}min"
        return duration



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

    