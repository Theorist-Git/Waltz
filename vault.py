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

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from __init__ import db
from models import Passwords
from dotenv import load_dotenv
from os import environ

load_dotenv()
sender = environ['SENDER']
password = environ['PASSWORD']

vault = Blueprint("vault", __name__, template_folder="templates/vault_templates/")


@vault.route('/vault', methods=["GET", "POST"])
@login_required
def vault_display():
    Password_blob = Passwords.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        USERNAME = request.form['USERNAME']
        URL = request.form['URL']
        ENCRYPTED_PASSWORD = request.form['PASSWORD']

        new_entry = Passwords(
            user_id=current_user.id,
            user_name=USERNAME,
            url=URL,
            password=ENCRYPTED_PASSWORD
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("vault.vault_display"))

    return render_template("vault.html", Password_blob=Password_blob)
