from flask import Blueprint, render_template, request, flash, redirect, url_for
from gms.db import get_db
from flask import current_app

bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        dob = request.form['dob']
        membership_type = request.form['type']

        db = get_db()

        try:
            db.execute(
                "INSERT INTO Members (name, email, phone_number, dob, membership_type) VALUES (?, ?, ?, ?, ?)",
                (name, email, phone_number, dob, membership_type),
            )
            db.commit()
            current_app.logger.info(f'Member {name} with email {email} was successfully registered.')

        except db.IntegrityError:
            error = f"Member {name} with email {email} is already registered."
        else:
            return redirect(url_for("members.view"))

    return render_template('register.html')

@bp.route('/view')
def view():
    db = get_db()
    members = db.execute('SELECT * FROM members').fetchall()
    return render_template('register.html', members=members)

