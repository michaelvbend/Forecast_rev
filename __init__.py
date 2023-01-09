from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

bcrypt = Bcrypt()
bcr
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from model import db


    db.init_app(app)
    login_manager.init_app(app)
    return app

