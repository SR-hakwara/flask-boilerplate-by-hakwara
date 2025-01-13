from dataclasses import dataclass  # For declaring data classes with special methods (such as __init__)
from flask_login import UserMixin  # To manage user authentication with Flask-Login
from app.extensions import db 
from datetime import datetime, timedelta 
from typing import Optional 
from flask import current_app 

@dataclass
class User(UserMixin, db.Model):
    """Data model to represent a user in the database"""
    
    # Data model fields (columns) declaration 
    id: int = db.Column(db.Integer, primary_key=True)  # Primary key of the user record in the database 
    username: str = db.Column(db.String(80), unique=True, nullable=False)  # Username of the user unique and required
    password_hash: str = db.Column(db.String(128), nullable=False)  # Hashed password of the user
    created_at: datetime = db.Column(db.DateTime, default=datetime.now)  # Date and time of user creation
    last_login: Optional[datetime] = db.Column(db.DateTime) # Date and time of the last login
    login_attempts: int = db.Column(db.Integer, default=0)  # Number of login attempts
    locked_until: Optional[datetime] = db.Column(db.DateTime)  # Date and time until the account is locked
    
    def __repr__(self) -> str:
        """String representation of the User object"""
        return f"<User {self.username}>"

    def increment_login_attempts(self) -> None:
        """
        Increments the login attempts counter 
        and locks the account if the maximum number of login attempts is reached
        """
        self.login_attempts += 1
        if self.login_attempts >= current_app.config["MAX_LOGIN_ATTEMPTS"]:
            self.locked_until = datetime.now() + timedelta(
                seconds=current_app.config["LOGIN_ATTEMPT_TIMEOUT"]
            )
        db.session.commit()

    def reset_login_attempts(self) -> None:
        """Resets the login attempts counter and unlocks the account"""
        self.login_attempts = 0
        self.locked_until = None
        db.session.commit()

    def update_last_login(self) -> None:
        """Updates the last login date and time"""
        self.last_login = datetime.now()
        db.session.commit()

    def is_locked(self) -> bool:
        """
        Checks if the user account is locked
        :return: True if the account is locked, False otherwise
        """
        return self.locked_until and self.locked_until > datetime.now()