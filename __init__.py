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

from flask import Flask, render_template, url_for, flash
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

# We define an SQLAlchemy object
db = SQLAlchemy()
user = current_user


def create_app():
    """
    This function creates app the ready to run, it takes care of all the configuration settings
    of the app. It handles all the database relational models, login managers, view blueprint
    registration, error handling and admin panel & related views.
    :return: app (An instance of Flask)
    """
    app = Flask(__name__)
    admin = Admin(app, name="Theorist", template_mode="bootstrap4")

    CSRFProtect(app)
    load_dotenv()

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://theorist:%s@localhost/theorist_dev' % \
                              quote(environ['THEORIST_LOCALHOST_PASS'])

    # 256 bit security key
    app.config['WTF_CSRF_SECRET_KEY'] = environ['WTF_CSRF_SECRET_KEY']
    app.config['SECRET_KEY'] = environ['SECRET_KEY']
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = "Lax"
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # The session will time out after 720 minutes or 12 hours
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=720)
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    # This callback can be used to initialize an application for the
    # use with this database setup.  Never use a database in the context
    # of an application not initialized that way or connections will
    # leak.

    db.init_app(app)

    # importing view blueprints from their respective files, to be registered with the flask app.
    from auth import auth
    from vault import vault

    # To be fixed after views are fixed!!!
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(vault, url_prefix='/')

    # 'app.errorhandler' decorator overrides default error pages and replaces them with custom ones
    # 404(page_not_found), 403(forbidden), 500(internal server error) are set explicitly
    @app.errorhandler(404)
    def page_not_found(_):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(_):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(_):
        return render_template('500.html'), 500

    # Importing database model (see models.py).
    from models import User, Passwords

    # Will create tables if they're not there
    with app.app_context():
        db.create_all()

    # Adding admin views
    class MyAdminViews(ModelView):
        def is_accessible(self):
            """
            is_accessible method is overridden method in BaseView and make it so that only users that
            are authenticated and have an "admin" role can access admin views.
            :return: Boolean (True -> is_accessible) & (False -> is_not_accessible)
            """
            if current_user.is_authenticated:
                admin_user = User.query.get(current_user.id)
                res = (admin_user.role == "admin")
                return res

        def inaccessible_callback(self, name, **kwargs):
            """
            redirect to login page if user doesn't have access
            """
            flash("Forbidden 403", category="error")
            return redirect(url_for('auth.login'))

    # Adding views to Admin Panel (An instance of Admin class in flask_admin)
    admin.add_view((MyAdminViews(User, db.session)))
    admin.add_view((MyAdminViews(Passwords, db.session)))

    # To use flask-login to manage authentication ,we create an instance of LoginManager Class in flask-login.
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
