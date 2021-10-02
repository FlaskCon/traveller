from modules.box__default.auth.models import User
from init import ModelForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import  TextField
#from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import InputRequired
#from wtforms.validators import Length
#from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from sqlalchemy import func


def validate_email(self, field):
    user = User.query.filter(
        func.lower(User.email) == func.lower(field.data)
        ).scalar()
    if user is not None:
        raise ValidationError(f"email '{field.data}' is already in use.")


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        #all relations not included by default wtforms-alchemy behaviour
        exclude = ['username', '_password', 'is_admin', #'date_registered',
                    'is_email_confirmed', 'email_confirm_date', 'bio',]
                    #'roles']
        field_args = {
            'first_name': {
                'render_kw': {
                    'autocomplete': 'off',
                    'class': 'border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150'
                }
            },
            'last_name': {
                'render_kw': {
                    'cols': 80,
                    'class': 'border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150'
                }
            },
            'email': {
                'render_kw': {
                    'cols': 80,
                    'class': 'border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150'
                },
            }
           
        }
        
