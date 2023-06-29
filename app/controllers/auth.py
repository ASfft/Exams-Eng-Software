from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from app.factory import app, db
from app.models import User

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Here, you would handle the login form and authenticate the user
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))