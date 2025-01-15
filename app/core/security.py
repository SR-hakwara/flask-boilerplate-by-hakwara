from app.extensions import bcrypt
from bcrypt import checkpw


class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password"""
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
