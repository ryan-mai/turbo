from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .extensions import db, login_manager
from .utils import is_strong_password
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            if is_strong_password(password):
                hashed_pw = generate_password_hash(password)
                new_user = User(username=username, password=hashed_pw)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.', 'danger')
    return render_template('register.html')

# Google OAuth
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    redirect_url="/login/google/authorized"
)

# GitHub OAuth
github_bp = make_github_blueprint(
    client_id=os.getenv("GITHUB_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
    redirect_url="/login/github/authorized"
)

@auth_bp.route("/login/google/authorized")
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()
    username = info["email"]
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password=generate_password_hash(os.urandom(16)))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("Logged in with Google!", "success")
    return redirect(url_for("dashboard"))

@auth_bp.route("/login/github/authorized")
def github_authorized():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    info = resp.json()
    username = info["login"]
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password=generate_password_hash(os.urandom(16)))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("Logged in with GitHub!", "success")
    return redirect(url_for("dashboard"))