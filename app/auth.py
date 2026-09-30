from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['name'].strip(); email=request.form['email'].strip().lower(); password=request.form['password']
        if User.query.filter_by(email=email).first(): flash('Email already registered.','danger'); return redirect(url_for('auth.register'))
        db.session.add(User(name=name,email=email,password_hash=generate_password_hash(password))); db.session.commit()
        flash('Registration successful. Please login.','success'); return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=User.query.filter_by(email=request.form['email'].strip().lower()).first()
        if user and check_password_hash(user.password_hash,request.form['password']):
            login_user(user); return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.','danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout(): logout_user(); return redirect(url_for('auth.login'))
