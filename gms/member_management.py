from flask import Blueprint, render_template, request, flash, redirect, url_for
from gms.db import get_db

bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        membership_type = request.form['type']
        db = get_db()
        error = None

        # Add more validation checks as required
        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        # ... add more validation checks as required ...

        if error is None:
            try:
                db.execute(
                    "INSERT INTO members (name, email, phone, dob, type) VALUES (?, ?, ?, ?, ?)",
                    (name, email, phone, dob, membership_type),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Member {name} with email {email} is already registered."
            else:
                return redirect(url_for("members.view"))
        flash(error)

    return render_template('register.html')

@bp.route('/view')
def view():
    db = get_db()
    members = db.execute('SELECT * FROM members').fetchall()
    return render_template('register.html', members=members)
