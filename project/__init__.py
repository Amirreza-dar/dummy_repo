from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from .models import User
from .database import db
from flask_login import LoginManager
from flask_migrate import Migrate

# import socketIO and events
from .logic import socketio


# init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # initializing socketIO
    socketio.init_app(app)

    return app

