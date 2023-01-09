from flask_login import UserMixin
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    predictions = db.relationship('Predictions', backref='user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_pass):
        return bcrypt.check_password_hash(self.password_hash, attempted_pass)

class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prediction_name = db.Column(db.String)
    prediction_value = db.Column(db.Float)
    prediction_campaign = db.Column(db.String)
    predicted_column = db.Column(db.String)
    coefficient = db.Column(db.Float)
    intercept = db.Column(db.Float)
    mae = db.Column(db.Float)
    mse = db.Column(db.Float)
    rmse = db.Column(db.Float)
    r2 = db.Column(db.Float)
    correlation = db.Column(db.Float)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))






