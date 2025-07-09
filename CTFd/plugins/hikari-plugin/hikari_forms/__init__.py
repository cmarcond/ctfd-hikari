from flask import render_template, redirect, url_for
from flask_babel import lazy_gettext as _l
from wtforms.validators import InputRequired, DataRequired
from wtforms import PasswordField, TextAreaField, StringField, FileField, SelectMultipleField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from CTFd.models import db, Teams
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import (
    attach_custom_user_fields,
    attach_registration_code_field,
    attach_user_bracket_field,
    build_custom_user_fields,
    build_registration_code_field,
    build_user_bracket_field,
)

from wtforms import SelectField
from CTFd.plugins.hikari_challenge import HikariChallengeModel
from CTFd.forms import CTFdCSRF

import enum

# Form for sending notifications to all competitors
def NotifyCompetitorsForm(*args, **kwargs):
    class _NotifyCompetitorsForm(BaseForm):
        textArea = TextAreaField(_l('Message'), validators=[InputRequired()])
        submit = SubmitField(_l('Send Email'))

    return _NotifyCompetitorsForm(*args, **kwargs)

def NotifyMultipleCompetitorsForm(*args, **kwargs):
    teams = Teams.query.all()
    team_choices = list()
    for team in teams:
        team_choices.append((str(team.id), team.name))

    class _NotifyCompetitorsForm(BaseForm):
        message = TextAreaField('Message', id='message-area' ,validators=[InputRequired()])
        team_selection = SelectMultipleField('Select team', id='team-selection-field', choices=team_choices ,validators=[InputRequired()])
        submit = SubmitField('Notify Team(s)')

    return _NotifyCompetitorsForm(*args, **kwargs)



# Form for registering zerotiers
def ZerotierForm(*args, **kwargs):
    class _ZerotierForm(BaseForm):
        network_id = StringField('Network ID', validators=[DataRequired()])
        name = StringField('Name', validators=[DataRequired()])
        submit = SubmitField('Submit')

    return _ZerotierForm(*args, **kwargs)


def SetupFirstChallengeForm(*args, **kwargs):
    challs = HikariChallengeModel.query.all()
    chall_choices = [(str(c.id), c.name) for c in challs]

    class _SetupFirstChallengeForm(BaseForm):
        challenge_selection = SelectField('Select challenge', id='chall-selection-field', choices=chall_choices ,validators=[InputRequired()])
        submit = SubmitField('Setup')

    return _SetupFirstChallengeForm(*args, **kwargs)



def ImportHikariCTFdForm(*args, **kwargs):
    class _ImportHikariCTFdForm(FlaskForm):
        class Meta:
            csrf = True
            csrf_class = CTFdCSRF
            csrf_field_name = "nonce"
        file_import = FileField('Zip file of exported competition', validators=[DataRequired()])
        submit = SubmitField('Setup')

    return _ImportHikariCTFdForm(*args, **kwargs)


