# Ice Skating Club Sign-In App  

The Ice Skating Club Sign-In App helps the ice skating club efficiently manage member sign-ins, track attendance for specific meetings, and maintain overall attendance records. I built this with Flask and SQLAlchemy, with the chief features being meeting management and a comprehensive admin dashboard.


## Using the App  

When you open the app, the first page you encounter is the **Sign-In Page**. Members can sign in simply by entering their name into the input field and clicking the sign-in button. Each sign-in is automatically recorded with the current date and time. If a member is signing in for the first time, their name will be added to the database, ensuring they are recognized in future attendance records.  

Admins have additional privileges. From the **Sign-In Page**, admins can access the **Admin Login** button to securely log in and unlock features such as creating meetings and viewing attendance statistics. Admins must log in to access the **Admin Dashboard** and **Meeting Management** pages.  

Once logged in, the **Admin Dashboard** is the primary interface for monitoring attendance. Here, admins can view the total number of times each member has signed in, as well as a detailed breakdown of attendees for each specific meeting. The dashboard provides a comprehensive overview of participation trends and helps identify active members.  

To manage meetings, navigate to the **Meeting Management** page by clicking the "See Meetings" button on the dashboard. On this page, admins can create new meetings by specifying the date, time, and topic. After creating a meeting, it will appear in the list of all scheduled meetings. Clicking on a specific meeting link takes you to the meeting’s details page, where you can view a list of attendees who signed in for that meeting, along with the timestamps of their sign-ins.  

The app is designed to be intuitive and easy to navigate. Members only need to enter their name on the home page to log their attendance, while admins have a streamlined workflow for managing meetings and viewing attendance statistics. By providing these features in a simple and accessible manner, the Ice Skating Club Sign-In App ensures efficient record-keeping and meeting management for the club.

---

## Setting Up the App  

To set up and run the app, you will need Python 3.7 or higher. Start by cloning the repository and navigating to the project directory. Create a virtual environment, activate it, and install the required dependencies listed in the `requirements.txt` file. Next, initialize the database using Flask-Migrate by running `flask db init`, followed by `flask db migrate` and `flask db upgrade` to set up the schema. Once the database is ready, start the app by running `flask run`, and access it in your browser at `http://127.0.0.1:5000/`.  

With the app running, you can immediately begin using the sign-in functionality on the home page. Admins can log in to access additional features, create meetings, and monitor attendance using the dashboard. The simple setup process ensures that the app is ready for use in just a few steps.

---

This documentation should provide all the guidance needed to navigate the app effectively, starting from the sign-in page and progressing to the admin dashboard and meeting management. If any questions arise, the step-by-step instructions will help resolve them quickly.
