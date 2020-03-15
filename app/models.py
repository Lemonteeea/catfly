from datetime import datetime
from app import db
from app import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    category = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(30), default = "Catfly")


