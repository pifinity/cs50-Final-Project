from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Member, SignIn, Meeting
from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime, timedelta
from sqlalchemy import and_

# Initialize the Flask app and configure the database and secret key
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db.init_app(app)

# Route for the home page (member sign-in)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the name from the form and strip extra whitespace
        name = request.form.get('name').strip()
        
        # Check if the name field is empty
        if not name:
            flash('Name is required!', 'danger')
            return redirect(url_for('index'))
        
        # Check if the member exists in the database
        member = Member.query.filter_by(name=name).first()
        if not member:
            # Create a new member if they don't already exist
            member = Member(name=name)
            db.session.add(member)
        
        # Record the sign-in for today
        today = datetime.utcnow().date()
        # Check if the member has already signed in today
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
            # Add a new sign-in record for the member
            sign_in = SignIn(member=member)
            db.session.add(sign_in)
            db.session.commit()
            flash(f'{name} has signed in successfully!', 'success')

        return redirect(url_for('index'))

    # Render the sign-in page
    return render_template('index.html')

# Route for the admin dashboard
@app.route('/dashboard')
def dashboard():
    # Ensure the user is logged in as an admin
    if not session.get('admin'):
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('index'))

    # Fetch all members and calculate their total attendance
    members = Member.query.all()
    attendance = {member.name: len(member.sign_ins) for member in members}

    # Fetch all meetings and their attendees
    meetings = Meeting.query.order_by(Meeting.date).all()

    # Render the dashboard template with attendance and meeting data
    return render_template('dashboard.html', attendance=attendance, meetings=meetings)

# Route to log out the admin
@app.route('/logout')
def logout():
    # Remove the admin session and redirect to the home page
    session.pop('admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# Route for the admin login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve the password from the form
        password = request.form.get('password')
        if password == 'password':  # Replace with a more secure password
            # Set the admin session if the password is correct
            session['admin'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password.', 'danger')
    # Render the login page
    return render_template('login.html')

# Route to create and view meetings
@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
    if request.method == 'POST':
        # Retrieve meeting details from the form
        topic = request.form.get('topic')
        date = request.form.get('date')
        time = request.form.get('time')

        # Validate that date and time are provided
        if not date or not time:
            flash('Date and time are required for a meeting.', 'danger')
            return redirect(url_for('meetings'))

        # Combine date and time into a single datetime object
        meeting_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        # Create a new meeting and save it to the database
        meeting = Meeting(date=meeting_datetime, topic=topic)
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting created successfully!', 'success')
        return redirect(url_for('meetings'))

    # Fetch all meetings to display
    all_meetings = Meeting.query.order_by(Meeting.date).all()
    return render_template('meetings.html', meetings=all_meetings)

# Route to view details of a specific meeting and sign-in attendees
@app.route('/meetings/<int:meeting_id>', methods=['GET', 'POST'])
def meeting_detail(meeting_id):
    # Fetch the meeting by its ID or return a 404 error
    meeting = Meeting.query.get_or_404(meeting_id)
    if request.method == 'POST':
        # Retrieve the member's name from the form
        name = request.form.get('name').strip()
        # Find or create the member
        member = Member.query.filter_by(name=name).first()
        if not member:
            member = Member(name=name)
            db.session.add(member)
        
        # Record the member's sign-in for this meeting
        sign_in = SignIn(member=member, meeting=meeting)
        db.session.add(sign_in)
        db.session.commit()
        flash(f'{name} signed in for meeting "{meeting.topic}"!', 'success')
        return redirect(url_for('meeting_detail', meeting_id=meeting.id))

    # Fetch attendees for the meeting
    attendees = [(sign_in.member.name, sign_in.timestamp) for sign_in in meeting.attendees]
    # Render the meeting detail page with attendee data
    return render_template('meeting_detail.html', meeting=meeting, attendees=attendees)

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
