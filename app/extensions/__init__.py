"""
Flask extensions centralization module.
Initialize all Flask extensions here to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from flask_mail import Mail
# from flask_caching import Cache

# Database ORM
db = SQLAlchemy()

# Database migrations
migrate = Migrate()

# Password hashing
bcrypt = Bcrypt()

# User session management
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "Please log in to access this page."

# Email support
# mail = Mail()
# Application caching
# cache = Cache()


def init_extensions(app):
    """
    Initialize all Flask extensions.

    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # mail.init_app(app)
    # cache.init_app(app)

    # Login manager configuration to load users
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(int(user_id))
