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

    filter_email = request.args.get('filter_email', '')
    filter_phone = request.args.get('filter_phone', '')
    filter_type = request.args.get('filter_type', '')

    query = 'SELECT * FROM members WHERE 1=1'
    parameters = {}

    if filter_email:
        query += ' AND email = :filter_email'
        parameters['filter_email'] = filter_email

    if filter_phone:
        query += ' AND phone_number = :filter_phone'
        parameters['filter_phone'] = filter_phone

    if filter_type:
        query += ' AND membership_type = :filter_type'
        parameters['filter_type'] = filter_type

    members = db.execute(query, parameters).fetchall()
    return render_template('register.html', members=members)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    db = get_db()
    member = db.execute('SELECT * FROM Members WHERE member_id = ?', (id,)).fetchone()

    if member is None:
        flash('Member not found.')
        return redirect(url_for('members.view'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        dob = request.form['dob']
        membership_type = request.form['type']
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'

        if error is not None:
            flash(error)
        else:
            try:
                db.execute(
                    'UPDATE Members SET name = ?, email = ?, phone_number = ?, dob = ?, membership_type = ?'
                    ' WHERE member_id = ?',
                    (name, email, phone_number, dob, membership_type, id)
                )
                db.commit()
                flash('Member updated successfully.')
                return redirect(url_for('members.view'))
            except db.IntegrityError as e:
                flash(f'An error occurred: {e}.')
                return redirect(url_for('members.edit', id=id))

    return render_template('edit.html', member=member)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM Members WHERE member_id = ?', (id,))
    db.commit()
    flash('Member successfully deleted.')
    return redirect(url_for('members.view'))


@bp.route('/class_enrollment', methods=['GET'])
def class_enrollment():
    db = get_db()
    # Retrieve filter parameters from the request's query string
    filter_start_date = request.args.get('start_date')
    filter_end_date = request.args.get('end_date')
    filter_trainer = request.args.get('trainer')

    query = """
    SELECT Classes.class_id, Classes.class_name, Classes.description, Classes.class_date, 
           Trainers.name as trainer_name, Classes.schedule_time, Classes.duration, Classes.max_members
    FROM Classes
    JOIN Trainers ON Classes.trainer_id = Trainers.trainer_id
    WHERE (COALESCE(:start_date, '') = '' OR Classes.class_date >= :start_date)
    AND (COALESCE(:end_date, '') = '' OR Classes.class_date <= :end_date)
    AND (COALESCE(:trainer, '') = '' OR Trainers.name LIKE :trainer)
    ORDER BY Classes.class_date, Classes.schedule_time
    """
    classes = db.execute(query, {
        'start_date': filter_start_date,
        'end_date': filter_end_date,
        'trainer': f'%{filter_trainer}%' if filter_trainer else None,
    }).fetchall()

    total_classes = len(classes)
    average_duration = round(sum(c['duration'] for c in classes) / total_classes, 1) if classes else 0
    average_members = round(sum(c['max_members'] for c in classes) / total_classes, 1) if classes else 0

    return render_template('class_enrollment.html', classes=classes, total_classes=total_classes,
                           average_duration=average_duration, average_members=average_members)
