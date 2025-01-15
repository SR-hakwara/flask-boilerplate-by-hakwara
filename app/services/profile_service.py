from typing import Optional
from dataclasses import dataclass
from app.models import User
from app.extensions import db
from app.core.security import SecurityUtils

@dataclass
class ProfileUpdateResult:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None

class ProfileService:
    @staticmethod
    def update_profile(user_id: int, form_data: dict) -> ProfileUpdateResult:
        """Met à jour les informations du profil utilisateur."""
        try:
            user = User.query.get(user_id)
            if not user:
                return ProfileUpdateResult(success=False, error="Utilisateur non trouvé")

            # Vérifie si le nouveau nom d'utilisateur ou email est déjà utilisé
            if 'username' in form_data:
                existing_user = User.query.filter(User.username == form_data['username'], User.id != user_id).first()
                if existing_user:
                    return ProfileUpdateResult(success=False, error="Ce nom d'utilisateur est déjà utilisé")

            if 'email' in form_data:
                existing_email = User.query.filter(User.email == form_data['email'], User.id != user_id).first()
                if existing_email:
                    return ProfileUpdateResult(success=False, error="Cet email est déjà utilisé")

            # Met à jour les champs
            if 'username' in form_data:
                user.username = form_data['username']
            if 'email' in form_data:
                user.email = form_data['email']
            if 'password' in form_data and form_data['password']:
                user.password_hash = SecurityUtils.hash_password(form_data['password'])

            db.session.commit()
            return ProfileUpdateResult(success=True, user=user)

        except Exception as e:
            db.session.rollback()
            return ProfileUpdateResult(success=False, error=f"Erreur lors de la mise à jour du profil : {str(e)}")