from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Simple login form with basic validation"""

    login = StringField(
        "Email or Username", validators=[DataRequired(), Length(min=3, max=120)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    """Registration form with basic field validation"""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=72)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    accept_tos = BooleanField(
        "I accept the Terms of Service", validators=[DataRequired()]
    )
