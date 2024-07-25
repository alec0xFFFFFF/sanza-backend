from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from sqlalchemy.ext.declarative import declarative_base
from posthog import Posthog

db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()
posthog = Posthog(
    project_api_key=Config.POSTHOG_KEY,
    host=Config.POSTHOG_URL
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        if db.engine.url.drivername == 'postgresql':
            db.engine.execute('CREATE EXTENSION IF NOT EXISTS vector')

    from app.routes import auth, recipes
    app.register_blueprint(auth.bp)
    app.register_blueprint(recipes.bp)

    return app
