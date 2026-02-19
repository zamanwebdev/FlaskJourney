from flask import Flask
from .routes import main
from .config import Config
from .models import create_users_table

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_users_table()

    app.register_blueprint(main)

    return app
