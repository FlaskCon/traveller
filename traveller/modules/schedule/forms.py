from datetime import datetime as dt

from modules.schedule.models import Day
from modules.schedule.models import Activity
from modules.conf.models import Talk

from init import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired


class DayForm(ModelForm):
    class Meta:
        model = Day


class NormalActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type']
        field_args = {
            'text': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'start_time': {
                'render_kw': {
                    'min': "09:00",
                    'max': "18:00",
                    'step': "1800",
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'end_time': {
                'render_kw': {
                    'min': "09:00",
                    'max': "18:00",
                    'step': "1800",
                    'autocomplete': 'off',
                    'required':''
                }
            }
        }


class TalkActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['talk_id', 'type', 'text']

        field_args = {
            'start_time': {
                'render_kw': {
                    'min': "09:00",
                    'max': "18:00",
                    'step': "1800",
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'end_time': {
                'render_kw': {'min': "09:00",
                    'max': "18:00",
                    'step': "1800",
                    'autocomplete': 'off',
                    'required':''
                }
            }
        }


    talks = QuerySelectField(
        'Talk:',
        validators = [InputRequired()],
        query_factory=lambda: Talk.query.filter(
            Talk.year == dt.utcnow().year,
            Talk.accepted == 'accepted'
            ).all(),
        render_kw={
            'class': "max-w-md"
        }
    )
    