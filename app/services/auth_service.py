from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
from app.models import User
from app.extensions import db
from app.core.security import SecurityUtils

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
                username=form_data['username'],
                email=form_data['email'],
                password_hash=SecurityUtils.hash_password(form_data['password']),
                created_at=datetime.now()
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
            if '@' in form_data['login']:
                user = User.query.filter_by(email=form_data['login']).first()
            else:
                user = User.query.filter_by(username=form_data['login']).first()

            if not user:
                return AuthResult(success=False, error="Invalid credentials")

            if not SecurityUtils.verify_password(form_data['password'], user.password_hash):
                return AuthResult(success=False, error="Invalid credentials")

            return AuthResult(success=True, user=user)
        except Exception as e:
            return AuthResult(success=False, error=f"Login failed: {str(e)}")