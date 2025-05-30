from flask import Flask
from .extensions import db, login_manager
from .models import User
from .auth import auth_bp, google_bp, github_bp
from .routes import main_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change_this_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(google_bp, url_prefix="/login")
app.register_blueprint(github_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)