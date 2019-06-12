
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    college = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    quiz = db.relationship('Quiz', backref='user', uselist=False)
    machine_no = db.relationship('Practical', uselist=False, backref='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.college}')"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Quiz('{self.user_id}', '{self.score}')"

class Practical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    machine_no = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f"Quiz('{self.user_id}', '{self.machine_no}')"

