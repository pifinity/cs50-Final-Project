# Ice Skating Club Sign-In App  
I built this using Flask and SQLAlchemy. It helps the ice skating club keep track of member sign-ins for weekly meetings, track attendance for specific meetings, and manage overall attendance records.  

## Features
### Member Sign-In:  
Allows members to sign in with their names.  
Automatically records the date and time of the sign-in.  

### Meeting Management:  
Admins can create meetings with specific dates, times, and topics.  
Tracks which members attended each meeting.  

### Attendance Dashboard:  
Displays overall attendance for each member.  
Displays a breakdown of attendees for each meeting.  


## Installation Prerequisites  
Python 3.7 or higher  
Flask  
SQLAlchemy  
Flask-Migrate (optional, for database migrations)  

## Instructions on how to run app:  

### Clone the repository:  
git clone <repository-url>  
cd ice_skating_club  

### Create and activate a virtual environment:  
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  


### Install dependencies:  
pip install -r requirements.txt  

### Set up the database:  
flask db init  
flask db migrate -m "Initial migration"  
flask db upgrade  

### Run the application:  
flask run  

Open your browser and navigate to:  
http://127.0.0.1:5000/  

# Usage
## Sign-In
At the landing page, you will need to login in order to access the app. Visit the home page and sign in through Admin Login to gain access to the rest of the information.

## Dashboard
Navigate to /dashboard to view the admin dashboard.  
Log in as an admin to create and manage meetings.  
Meeting Management  
Navigate to /meetings to create new meetings.  
View attendees for each meeting by clicking on a meeting link.  
