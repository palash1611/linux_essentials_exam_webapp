
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
    quiz = db.relationship('Quiz', backref='student', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.college}')"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    q1 = db.Column(db.String(100), nullable=False)
    q2 = db.Column(db.String(100), nullable=False)
    q3 = db.Column(db.String(100), nullable=False)
    q4 = db.Column(db.String(100), nullable=False)
    q5 = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Quiz('{self.user_id}', '{self.q1}', '{self.q2}', '{self.q3}', '{self.q4}', '{self.q5}')"

