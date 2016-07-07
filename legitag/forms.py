from wtforms import Form, BooleanField, TextField, StringField, RadioField, HiddenField, TextAreaField, validators, ValidationError, FieldList
from wtforms.widgets import TextArea
from flask_security.forms import RegisterForm

class TagForm(Form):
    policy_area_tags = TextField('What policy areas might it cover?', widget=TextArea())
    users_affected_tags = TextField('Who might it affect?', widget=TextArea())

class RegisterUserForm(RegisterForm):
    name = StringField('Name', [validators.Required()])