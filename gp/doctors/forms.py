from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed, FileField

from flask_login import current_user
from gp.models import Doctor


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")




class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("UserName", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords must match!"),
        ],
    )
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    specialization = SelectField('Specialization', choices=[('Radiologist', 'Radiologist'), ('Neurologist', 'Neurologist')])
    submit = SubmitField("Register!")


# class UpdateUserForm(FlaskForm):
#     name = StringField('Username', validators=[DataRequired()])
#     profile = FileField('Update Profile Picteure', validators=[FileAllowed(['png', 'jpg',])])
#     submit = SubmitField('Update')