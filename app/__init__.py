from datetime import datetime
from flask import Flask
from .extensions import db, login_manager, bcrypt, migrate

def create_app(config_object=None):

    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    from .routes import auth_bp, main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from .models import User

    # Tell Flask-Login how to load a user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Inject the current time into all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now}

    return app





