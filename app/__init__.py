import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, login_manager
load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','dev-secret-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path,'fitbuddy.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app); login_manager.init_app(app); login_manager.login_view='auth.login'
    from .models import User
    from .auth import auth_bp
    from .main import main_bp
    app.register_blueprint(auth_bp); app.register_blueprint(main_bp)
    @login_manager.user_loader
    def load_user(user_id): return User.query.get(int(user_id))
    with app.app_context():
        db.create_all()
        from werkzeug.security import generate_password_hash
        if not User.query.filter_by(email='admin@fitbuddy.local').first():
            db.session.add(User(name='Fit Buddy Admin',email='admin@fitbuddy.local',password_hash=generate_password_hash('admin123'),role='admin'))
            db.session.commit()
    return app
