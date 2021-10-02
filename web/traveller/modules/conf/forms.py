from modules.conf.models import Conf
from init import ModelForm


class ConfForm(ModelForm):
    class Meta:
        model = Conf