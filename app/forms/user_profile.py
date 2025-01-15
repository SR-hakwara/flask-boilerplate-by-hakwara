from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class UserProfileForm(FlaskForm):
    """Form to update user profile information."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "New Password",
        validators=[Optional(), Length(min=8, max=72)],
    )
    confirm_password = PasswordField(
        "Confirme New Password",
        validators=[
            Optional(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
