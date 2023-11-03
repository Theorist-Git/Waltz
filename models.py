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

from __init__ import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    User class inherits UserMixin class from flask_login.
    db is an instance of SQLAlchemy(). [See __init__.py]
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    master_password = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    active = db.Column(db.Boolean)
    last_confirmed_at = db.Column(db.DateTime())
    two_FA = db.Column(db.Boolean, default=False, nullable=False)
    two_FA_key = db.Column(db.String(128), default=None, nullable=True)
    two_FA_type = db.Column(db.String(5), default=None, nullable=True)
    role = db.Column(db.String(6), default="user", nullable=False)

    passwords = db.relationship('Passwords')


class Passwords(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(128), default=None)
    url = db.Column(db.String(128), default=None)
    password = db.Column(db.String(150))
