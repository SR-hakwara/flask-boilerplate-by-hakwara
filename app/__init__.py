from datetime import datetime
from flask import Flask
from .extensions import init_extensions


def create_app(config_object=None):

    app = Flask(__name__)
    app.config.from_object(config_object)
    init_extensions(app)

    from .routes import auth_bp, main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Inject the current time into all templates
    @app.context_processor
    def inject_now():
        return {"now": datetime.now}

    return app
