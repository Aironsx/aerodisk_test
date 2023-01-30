from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from project.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from project.network_interface.routes import network_interface
    from project.users.routes import user

    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(network_interface, url_prefix='/network_interface')

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    from project.users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
