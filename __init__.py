"""
Waltz: An open source, cloud-based password manager.
Copyright (C) 2023 <Mayank Vats>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Flask, render_template, url_for, abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.utils import redirect
from urllib.parse import quote
from dotenv import load_dotenv
from os import environ

db = SQLAlchemy()
user = current_user


def create_app():
    """
    Configures the Flask application
    :return: app (An instance of Flask)
    """
    app = Flask(__name__)
    # Admin panel instantiated
    admin = Admin(app, name="Theorist", template_mode="bootstrap4")

    # CSRF Protection enabled globally.
    CSRFProtect(app)
    # Imports DB connection details from .env file.
    load_dotenv()

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % \
                              (
                                  quote(environ["USER"]),
                                  quote(environ["THEORIST_LOCALHOST_PASS"]),
                                  quote(environ["HOST"]),
                                  quote(environ["DB"])
                              )

    # WTF_CSRF_SECRET_KEY is used to generate a key that signs form POST requests.
    app.config["WTF_CSRF_SECRET_KEY"] = environ["WTF_CSRF_SECRET_KEY"]

    # A secret key that will be used for securely signing the session cookie.
    app.config["SECRET_KEY"] = environ["SECRET_KEY"]

    # Session cookie name.
    app.config["SESSION_COOKIE_NAME"] = "WALTZ_SESSION"

    # Browsers will only send cookies with requests over HTTPS if the cookie is marked “secure”.
    app.config["SESSION_COOKIE_SECURE"] = True

    # Lax prevents sending cookies with CSRF-prone requests from external sites, such as submitting a form.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Browsers will not allow JavaScript access to cookies marked as “HTTP only” for security.
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # Remember cookie
    app.config["REMEMBER_COOKIE_SECURE"] = True
    app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"
    app.config["REMEMBER_COOKIE_HTTPONLY"] = True

    # Providing SQlALCHEMY with the database URI.
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    # SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead.
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # User is automatically logged out after 5 minutes.
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)

    # Set optional bootswatch theme for the admin panel.
    app.config["FLASK_ADMIN_SWATCH"] = "darkly"

    db.init_app(app)

    # Importing blueprints
    from auth import auth
    from vault import vault

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(vault, url_prefix='/')

    # 'app.errorhandler' decorator overrides default error pages and replaces them with custom ones
    # 404(page_not_found), 403(forbidden), 500(internal server error) are set explicitly
    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden(_):
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def internal_server_error(_):
        return render_template("500.html"), 500

    # Importing database models (see models.py).
    from models import User, Passwords

    # Will create tables if they do not exist
    with app.app_context():
        db.create_all()

    # Restricting access to admin panel
    class MyAdminViews(ModelView):
        def is_accessible(self):
            """
            Overrides in-built 'is_accessible' method.
            Only users with 'admin' role can access this page.
            :return: is_accessible (BOOLEAN)
            """
            if current_user.is_authenticated:
                admin_user = User.query.get(current_user.id)
                res = (admin_user.role == "admin")
                return res

        def inaccessible_callback(self, name, **kwargs):
            """
            If 'is_accessible' returns False, 'inaccessible_callback' raises 403.
            """
            return render_template("403.html"), 403

    # Adding DB tables to admin panel for easy viewing.
    admin.add_view((MyAdminViews(User, db.session)))
    admin.add_view((MyAdminViews(Passwords, db.session)))

    # To use flask-login to manage authentication, we create an instance of LoginManager Class in flask-login.
    # We also have to specify which view will handle authentication, in my case the view is auth.login.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"

    # Configures an application. This registers an `after_request` call, and
    # attaches this `LoginManager` to it as `app.login_manager`.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
