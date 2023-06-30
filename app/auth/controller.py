from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, logout_user, login_user

from app.auth.forms import RegistrationForm, LoginForm
from app.factory import db
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('That username is taken. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('auth/login'))
    return render_template('auth/register.jinja2', title='Register', form=form)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # You should check the hashed password
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.jinja2', title='Login', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

