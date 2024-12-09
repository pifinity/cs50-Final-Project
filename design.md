# DESIGN.md

## **Overview**

The Ice Skating Club Sign-In App is a web application built using Flask and SQLAlchemy. It was designed to streamline the process of tracking attendance at ice skating club meetings, manage meetings, and provide an intuitive admin dashboard for attendance statistics. The app emphasizes simplicity for end-users while maintaining flexibility and scalability for administrators.

## **Key Features and Design Decisions**

### **1. Core Functionality**
- **Member Sign-In**:
  - Members can sign in by simply entering their name on the home page.
  - The system uses a `Member` model to store user details, ensuring no duplicate names are added. If a user signs in for the first time, they are automatically added to the database.
  - Each sign-in is logged with a timestamp and optionally linked to a specific meeting.

- **Meeting Management**:
  - Admins can create meetings by specifying a date, time, and optional topic.
  - Each meeting is stored in the `Meeting` model, which is linked to `SignIn` entries via a `meeting_id` foreign key.
  - This relational design allows for granular tracking of attendance at specific meetings.

- **Admin Dashboard**:
  - Provides an overview of member attendance, with total counts per member.
  - Displays individual meetings and their attendees, offering visibility into participation trends.
  - Uses dynamic filtering and aggregation queries via SQLAlchemy to compute statistics efficiently.

### **2. Database Design**
The app uses SQLAlchemy ORM with the following models:

#### **Member**
```python
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    sign_ins = db.relationship('SignIn', backref='member', lazy=True)
```
- Members are uniquely identified by their names.
- A one-to-many relationship links members to their sign-ins.

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
- Stores metadata about each meeting.
- A one-to-many relationship links meetings to their attendees via `SignIn`.

### **3. Application Architecture**
The app adheres to a clean separation of concerns, with Flask routes handling HTTP requests, templates managing the front-end, and SQLAlchemy managing database interactions.

#### **Routes**
The app includes routes for:
- Home (`/`): Member sign-in.
- Admin Dashboard (`/dashboard`): View attendance statistics and meeting records.
- Meetings (`/meetings`): Create and view meetings.
- Meeting Detail (`/meetings/<meeting_id>`): View attendees for a specific meeting and allow sign-ins.

#### **Templates**
Templates are structured to ensure reusability and maintainability:
- **`base.html`**: A shared layout with navigation links.
- **`index.html`**: The sign-in page.
- **`dashboard.html`**: Displays attendance and meeting statistics.
- **`meetings.html`**: Allows admins to create and view meetings.
- **`meeting_detail.html`**: Displays meeting attendees and provides a sign-in form.

---

## **Design Decisions**

### **1. Framework Choice**
Flask was chosen for its lightweight nature, making it easy to quickly prototype and build the app. SQLAlchemy ORM complements Flask well, providing an abstraction over SQL for managing relational data.

### **2. Database Design**
The relational structure ensures that:
- Members and their sign-ins are efficiently linked.
- Meeting attendance is dynamically calculated via relationships, reducing redundancy and potential data inconsistencies.

### **3. Admin Authentication**
Basic session-based authentication was implemented for admin access. While simple, it provides adequate security for this use case. In a production setting, more robust authentication (e.g., OAuth or JWT) could be added.

### **4. User Interface**
The UI was kept simple to ensure ease of use:
- Members only need to enter their name to sign in.
- Admins can easily navigate between the dashboard and meeting management pages.

### **5. Extensibility**
The app was designed with future features in mind:
- Adding more fields (e.g., email) to the `Member` model.
- Exporting attendance data to CSV.
- Sending email notifications for meetings.

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

The Ice Skating Sign-In App is a robust and scalable solution for managing attendance at ice skating club meetings. The modular design allows for easy maintenance and extensibility, making it a valuable tool for club administrators.

--- 
