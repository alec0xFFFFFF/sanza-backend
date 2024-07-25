from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from sqlalchemy.ext.declarative import declarative_base
from .posthog_extension import PostHogExtension

db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()
posthog = PostHogExtension()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    posthog.init_app(app)

    api = Api(app, version='1.0', title='Sanza API', description='A simple API')

    with app.app_context():
        if db.engine.url.drivername == 'postgresql':
            db.engine.execute('CREATE EXTENSION IF NOT EXISTS vector')

    from app.routes.auth import api as auth_ns
    from app.routes.recipes import bp as recipes_bp
    from app.routes.auth import bp as auth_bp

    api.add_namespace(auth_ns)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(auth_bp)

    return app
