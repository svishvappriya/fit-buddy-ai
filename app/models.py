from datetime import datetime
from flask_login import UserMixin
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profiles = db.relationship('FitnessProfile', backref='user', lazy=True)
    plans = db.relationship('FitnessPlan', backref='user', lazy=True)

class FitnessProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.String(40), nullable=False)
    workout_days = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(300), default='')
    diet = db.Column(db.String(50), default='No Preference')
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)
    maintenance_calories = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FitnessPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), default='AI Fitness Plan')
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
