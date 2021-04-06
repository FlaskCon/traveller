from modules.conf.models import Talk
from init import ModelForm


class SubmitTalkForm(ModelForm):
    class Meta:
        model = Talk
        exclude = ['accepted', 'slug', 'submitter_id']
        field_args = {
            'title': {
                'render_kw': {
                    'autocomplete': 'off'
                }
            },
            'description': {
                'render_kw': {
                    'cols': 80
                }
            },
            'summary': {
                'render_kw': {
                    'cols': 80
                }
            },
            'notes': {
                'render_kw': {
                    'cols': 80
                }
            }
        }


class AdminTalkForm(ModelForm):
    class Meta:
        model = Talk
        exclude = ['submitter_id']
        field_args = {
            'title': {
                'render_kw': {
                    'autocomplete': 'off'
                }
            },
            'description': {
                'render_kw': {
                    'cols': 80
                }
            },
            'summary': {
                'render_kw': {
                    'cols': 80
                }
            },
            'notes': {
                'render_kw': {
                    'cols': 80
                }
            }
        }