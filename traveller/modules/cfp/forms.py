from modules.conf.models import Talk
from init import ModelForm


class SubmitTalkForm(ModelForm):
    class Meta:
        model = Talk
        exclude = ['accepted', 'slug', 'submitter_id', 'year']
        field_args = {
            'title': {
                'render_kw': {
                    'autocomplete': 'off',
                    'maxlength': 200,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)',
                    'class': 'talk-forms border-1 px-3 mb-4 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring  ease-linear transition-all duration-150'
                }
            },
            'description': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 3000,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)',
                    'class': 'talk-forms border-1 mb-4 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring  ease-linear transition-all duration-150'
                }
            },
            'summary': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 300,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)',
                    'class': 'talk-forms border-1 mb-4 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring  ease-linear transition-all duration-150'
                }
            },
            'notes': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 200,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)',
                    'class': 'talk-forms border-1 mb-4 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring  ease-linear transition-all duration-150'
                }
            },
            'level': {
                'render_kw': {
                    'class': 'border-1 mb-4 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring  ease-linear transition-all duration-150'
                }
            }
        }


class AdminTalkForm(ModelForm):
    class Meta:
        model = Talk
        exclude = ['submitter_id', 'slug', 'year']
        field_args = {
            'title': {
                'render_kw': {
                    'autocomplete': 'off',
                    'maxlength': 200,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)'
                }
            },
            'description': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 3000,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)'
                }
            },
            'summary': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 300,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)'
                }
            },
            'notes': {
                'render_kw': {
                    'cols': 80,
                    'maxlength': 200,
                    'onblur': 'remove_indicator(this)',
                    'onfocus': 'show_indicator(this)'
                }
            }
        }
