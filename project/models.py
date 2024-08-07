# from . import db
import json
from .database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean, default=False)
    # Relationship to UserSession
    sessions = db.relationship('UserSession', backref='user', lazy=True)

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to the User model
    session_data = db.Column(db.Text, nullable=False)  # Stores JSON serialized session data

    def set_session_data(self, data):
        self.session_data = json.dumps(data)

    def get_session_data(self):
        return json.loads(self.session_data)
