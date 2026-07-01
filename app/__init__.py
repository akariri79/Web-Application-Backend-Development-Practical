from flask import Flask
from config import Config
from .extensions import db, migrate
from app.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import register_routes
    register_routes(app)

    return app
