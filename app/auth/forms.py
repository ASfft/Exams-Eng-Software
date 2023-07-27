from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

from app.constants import UserTypes

user_types_choices = [(choice.value, choice.name.capitalize()) for choice in UserTypes]


class RegistrationForm(FlaskForm):
    user_type = SelectField("User Type", choices=user_types_choices, coerce=int)
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=4, max=72)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    user_type = SelectField("User Type", choices=user_types_choices, coerce=int)
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=72)])
    submit_button = SubmitField("Login")
