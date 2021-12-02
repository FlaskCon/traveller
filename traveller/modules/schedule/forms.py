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
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'end_time': {
                'render_kw': {
                    'min': "09:00",
                    'max': "18:00",
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'note': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'border-1 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm focus:outline-none focus:ring',
                    'maxlength': 1000,
                    'style':'width:90%; height:100px;'
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
                    'autocomplete': 'off',
                    'required':''
                }
            },
            'end_time': {
                'render_kw': {'min': "09:00",
                    'max': "18:00",
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
    