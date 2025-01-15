from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from app.models import User
from app.extensions import db
from app.core import SecurityUtils


@dataclass
class AuthResult:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class AuthService:
    def register(form_data: dict) -> AuthResult:
        """Handle user registration"""
        # Create new user
        try:
            new_user = User(
                username=form_data["username"],
                email=form_data["email"],
                password_hash=SecurityUtils.hash_password(form_data["password"]),
                created_at=datetime.now(),
            )
            db.session.add(new_user)
            db.session.commit()
            return AuthResult(success=True, user=new_user)
        except Exception as e:
            db.session.rollback()
            return AuthResult(success=False, error=f"Registration failed: {str(e)}")

    def login(form_data: dict) -> AuthResult:
        """Handle user login with validation"""
        try:
            # Check if login is email or username
            if "@" in form_data["login"]:
                user = User.query.filter_by(email=form_data["login"]).first()
            else:
                user = User.query.filter_by(username=form_data["login"]).first()

            if not user:
                return AuthResult(success=False, error="Invalid credentials")

            if not SecurityUtils.verify_password(
                form_data["password"], user.password_hash
            ):
                return AuthResult(success=False, error="Invalid credentials")

            return AuthResult(success=True, user=user)
        except Exception as e:
            return AuthResult(success=False, error=f"Login failed: {str(e)}")

    @staticmethod
    def update_profile(user_id: int, form_data: dict) -> AuthResult:
        """Met à jour les informations du profil utilisateur."""
        try:
            user = User.query.get(user_id)
            if not user:
                return AuthResult(success=False, error="Utilisateur non trouvé")

            # Vérifie si le nouveau nom d'utilisateur ou email est déjà utilisé
            if "username" in form_data:
                existing_user = User.query.filter(
                    User.username == form_data["username"], User.id != user_id
                ).first()
                if existing_user:
                    return AuthResult(
                        success=False, error="Ce nom d'utilisateur est déjà utilisé"
                    )

            if "email" in form_data:
                existing_email = User.query.filter(
                    User.email == form_data["email"], User.id != user_id
                ).first()
                if existing_email:
                    return AuthResult(success=False, error="Cet email est déjà utilisé")

            # Met à jour les champs
            if "username" in form_data:
                user.username = form_data["username"]
            if "email" in form_data:
                user.email = form_data["email"]
            if "password" in form_data and form_data["password"]:
                user.password_hash = SecurityUtils.hash_password(form_data["password"])

            db.session.commit()
            return AuthResult(success=True, user=user)

        except Exception as e:
            db.session.rollback()
            return AuthResult(
                success=False,
                error=f"Erreur lors de la mise à jour du profil : {str(e)}",
            )
