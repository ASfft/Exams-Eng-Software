import os
from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5


# init extensions
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')}"
    app.secret_key = "secret-key"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # init extensions
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap = Bootstrap5(app)

    from .auth.loaders import load_user

    from .auth.controller import bp as bp_auth
    from .exams.controller import bp as bp_exams
    from .questions.controller import bp as bp_questions
    from .reports.controller import bp as bp_reports

    app.register_blueprint(bp_auth, url_prefix=f"/{bp_auth.name}")
    app.register_blueprint(bp_exams, url_prefix=f"/{bp_exams.name}")
    app.register_blueprint(bp_questions, url_prefix=f"/{bp_questions.name}")
    app.register_blueprint(bp_reports, url_prefix=f"/{bp_reports.name}")

    """
    404 Page not found error default handler
    """

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error/404.jinja2", error=e), 404

    @app.route("/")
    @app.route("/home")
    def home():
        return redirect(url_for("auth.login"))

    return app
