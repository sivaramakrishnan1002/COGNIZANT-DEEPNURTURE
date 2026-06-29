from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from .courses import courses_bp
    app.register_blueprint(courses_bp)

    from .errors import register_error_handlers
    register_error_handlers(app)

    return app
