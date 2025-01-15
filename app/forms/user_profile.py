from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class UserProfileForm(FlaskForm):
    """Formulaire pour mettre à jour les informations du profil utilisateur."""

    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "Nouveau mot de passe",
        validators=[Optional(), Length(min=8, max=72)],
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[
            Optional(),
            EqualTo("password", message="Les mots de passe doivent correspondre"),
        ],
    )