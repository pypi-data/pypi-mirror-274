from django.forms import Form
from django.forms.fields import CharField


class EchoInput(Form):
    msg = CharField(max_length=16, required=True)
