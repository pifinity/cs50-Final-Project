from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Member, SignIn, Meeting
from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime, timedelta
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the name from the form
        name = request.form.get('name').strip()
        
        if not name:
            flash('Name is required!', 'danger')
            return redirect(url_for('index'))
        
        # Check if the member exists in the database
        member = Member.query.filter_by(name=name).first()
        if not member:
            # If not, create a new member
            member = Member(name=name)
            db.session.add(member)
        
        # Record the sign-in for today
        today = datetime.utcnow().date()
        existing_sign_in = SignIn.query.filter(
            and_(
                SignIn.member == member,
                SignIn.timestamp >= today,
                SignIn.timestamp < today + timedelta(days=1)
            )
        ).first()
        if existing_sign_in:
            flash(f'{name} has already signed in today.', 'warning')
        else:
            sign_in = SignIn(member=member)
            db.session.add(sign_in)
            db.session.commit()
            flash(f'{name} has signed in successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Fetch all members and calculate attendance
    members = Member.query.all()
    attendance = {member.name: len(member.sign_ins) for member in members}

    # Fetch all meetings and attendees
    meetings = Meeting.query.order_by(Meeting.date).all()

    return render_template('dashboard.html', attendance=attendance, meetings=meetings)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'password':  # secure password
            session['admin'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password.', 'danger')
    return render_template('login.html')

@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
    if request.method == 'POST':
        topic = request.form.get('topic')
        date = request.form.get('date')
        time = request.form.get('time')

        if not date or not time:
            flash('Date and time are required for a meeting.', 'danger')
            return redirect(url_for('meetings'))

        meeting_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        meeting = Meeting(date=meeting_datetime, topic=topic)
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting created successfully!', 'success')
        return redirect(url_for('meetings'))

    all_meetings = Meeting.query.order_by(Meeting.date).all()
    return render_template('meetings.html', meetings=all_meetings)

@app.route('/meetings/<int:meeting_id>', methods=['GET', 'POST'])
def meeting_detail(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    if request.method == 'POST':
        name = request.form.get('name').strip()
        member = Member.query.filter_by(name=name).first()
        if not member:
            member = Member(name=name)
            db.session.add(member)
        
        sign_in = SignIn(member=member, meeting=meeting)
        db.session.add(sign_in)
        db.session.commit()
        flash(f'{name} signed in for meeting "{meeting.topic}"!', 'success')
        return redirect(url_for('meeting_detail', meeting_id=meeting.id))

    attendees = [(sign_in.member.name, sign_in.timestamp) for sign_in in meeting.attendees]
    return render_template('meeting_detail.html', meeting=meeting, attendees=attendees)


if __name__ == '__main__':
    app.run(debug=True)