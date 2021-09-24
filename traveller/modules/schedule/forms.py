from modules.schedule.models import Day
from modules.schedule.models import Activity
from modules.conf.models import Talk

from init import ModelForm

import wtforms_alchemy
from wtforms_components.fields import TimeField


class DayForm(ModelForm):
    class Meta:
        model = Day


class NormalActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type']

    start_time = TimeField(label="start time")
    end_time = TimeField(label="end time")

class TalkActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type', 'text']

    start_time = TimeField(label="start time")
    end_time = TimeField(label="end time")

    talks = wtforms_alchemy.fields.QuerySelectField(
        'Talk',
        query_factory=lambda: Talk.query.filter(Talk.accepted == 'accepted').all()
    )
