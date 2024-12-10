# DESIGN.md

## **Overview**

The Ice Skating Club Sign-In App is a web application built using Flask and SQLAlchemy. When I started desgining this app, I talked with the head of the ice skating club to see what needs I should address. Taking in the needs of the club, I wanted to deisgn an app to track attendance at ice skating club meetings, manage meetings, and provide an intuitive admin dashboard for attendance statistics. The app would be simple for users (they would only need to input their name) while providing a complete overview of members and meetings for admins.

## **Key Features and Design Decisions**

### **1. Base Functionality**
The purpose of this app would be to keep track of the sign ins of ice skating club members. The app would save the time the user logged in, the meeting the user would be attending, and of course their name. My system  uses a `Member` model to store user details, ensuring no duplicate names are added. If a user signs in for the first time, they are automatically added to the database. Each sign-in is logged with a timestamp and optionally linked to a specific meeting.

- **Meeting Management**:
The admin has the ability create a meeting. When a certain meeting is selected, it'll show a sign in screen for outside users. When outside users log in, they will be associated with this meeting. Meetings can be specified with a date, time, and optional topic. Each meeting is stored in the `Meeting` model, which is linked to `SignIn` entries via a `meeting_id` foreign key. 

- **Admin Dashboard**:
The dashboard provides an overview of member attendance, with total counts per member. It displays individual meetings and their attendees, offering visibility into participation trends. It uses dynamic filtering and aggregation queries via SQLAlchemy to compute statistics efficiently.

### **2. Database Design**
The app uses SQLAlchemy ORM with the following models:

#### **Member**
```python
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    sign_ins = db.relationship('SignIn', backref='member', lazy=True)
```

#### **SignIn**
```python
class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=True)
```
- Tracks when a member signs in and whether it is associated with a specific meeting.
- A `timestamp` column ensures accurate record-keeping.

#### **Meeting**
```python
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    topic = db.Column(db.String(200), nullable=True)
    attendees = db.relationship('SignIn', backref='meeting', lazy=True)
```

### **3. Application Architecture**
Flask is used in the frontend to handle HTTP requests and templates. I am using SQLAlchemy in the backend to manage database interactions.

#### **Routes**
- Home (`/`): Member sign-in.
- Admin Dashboard (`/dashboard`): View attendance statistics and meeting records.
- Meetings (`/meetings`): Create and view meetings.
- Meeting Detail (`/meetings/<meeting_id>`): View attendees for a specific meeting and allow sign-ins.

#### **Templates**
- **`base.html`**: A shared layout with navigation links.
- **`index.html`**: sign-in page.
- **`dashboard.html`**: Displays attendance and meeting statistics.
- **`meetings.html`**: Allows admins to create and view meetings.
- **`meeting_detail.html`**: Displays meeting attendees and provides a sign-in form.

---

## **Design Decisions**

### **1. Framework Choice**
I chose flask because it is quick to set up. The app doesn't require heavy processing power, and flask is a capable lightweight framework 

### **3. Admin Loginn**
I implemented a log in for admin users. If not logged in, a user would not be able to view the dashboard or create meetings. While its good enough for now, for security in production, I could use OAuth and jwt. Otherwise this app doesn't require too much security. The main concern would be protecting user names. 



---

## **Challenges and Solutions**

1. **Duplicate Sign-Ins**:
   - To prevent duplicate sign-ins for the same member on the same day, queries were written to check existing sign-ins before saving.

2. **Meeting Association**:
   - Linking sign-ins to meetings required careful handling of relationships and foreign keys to avoid orphaned records.

3. **Data Migration**:
   - Flask-Migrate was used to manage schema changes during development without losing data.

---

## **Conclusion**

I think my ice skating sign in app has a lot of functionality and meets the goals I set out to do. It works without issue and could make a great addition to the ice skating club in the future.
