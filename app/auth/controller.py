from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user

from app.auth.forms import RegistrationForm
from app.factory import db
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)  # You should hash the password before storing it
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.jinja2', title='Register', form=form)
