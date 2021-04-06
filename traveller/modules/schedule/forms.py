from modules.schedule.models import Day
from modules.schedule.models import Activity
from modules.conf.models import Talk

from init import ModelForm

import wtforms_alchemy


class DayForm(ModelForm):
    class Meta:
        model = Day


class NormalActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type']


class TalkActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type', 'text']


    talks = wtforms_alchemy.fields.QuerySelectMultipleField('Talk', 
        query_factory=lambda: Talk.query.order_by(Talk.title).all()
        )
