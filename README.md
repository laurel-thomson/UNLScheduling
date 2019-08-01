# UNL Scheduling Website

This is a scheduling application created for Dr. Josh Brummer from the University of Nebraska, Lincoln Mathematics Department.  The purpose
of the web app is to streamline the process of scheduling students to work in the UNL Math Resource Center.  The website allows students
to mark their availability and scheduling preferences for each time slot in the resource center.  Teachers can then view a master scheduling
list, where each time slots contains all of the students that have marked that time slots as "available".  The teacher can then 
select which student(s) to schedule for the particular time slot.  Once the teacher releases the schedule, students are able to view
the published schedule.

One of the main benefits of the application is that it simplifies the process of keeping track of how many hours a student is required to work.  Different students have different scheduling requirements: graduate students work 2 slots per week, some undergraduates work 10
slots per week, others work 6, etc.  When a teacher schedules a student and they meet their scheduling requirement, all of the other
instances where that student can be scheduled are disabled until one of their slots are unscheduled.  This prevents a student from being
over or under scheduled.  Additionally, the web app allows teachers to view data on which students have submitted their preferences and
which have been scheduled.

Finally, this application was created with the intention that it could be expanded for use beyond the Math Resource Center.  Teachers in the
app can create different "rooms" with their own set of students and time slots and use the website to schedule these rooms or events.

## Test Website

A test version of the website is available for viewing at <a href="http://laurelthomson.pythonanywhere.com">laurelthomson.pythonanywhere.com</a>!

To view the test data that has already been entered, you can log in with a few of these dummy accounts:

username: teacher  
password: mypassword  


username: student1  
password: mypassword


username: student2  
password: mypassword

## Installation

### Prerequisites
<a href="https://www.python.org/downloads/">Python 3</a>  
<a href="https://pip.pypa.io/en/stable/">pip</a> - included by default with Python 3.4  

### Virtual Environment
Download or clone the repository and navigate to the root directory of the repo.  Make a virtualenv called `myvenv` that will isolate your Python/Django setup:  

**Windows**  
`python -m venv myvenv`  

**Linux/OS X**  
`$ python3 -m venv myvenv`

Start your virtualenv:

**Windows**  
`myvenv\Scripts\activate`

**Linux/OS X**  
`$ source myvenv/bin/activate`

If your virtualenv has been successfully activated, your console prompt will be prefaced with `(myvenv)`.

### Installing Requirements
Make sure that pip is up-to-date:  
`$ python -m pip install --upgrade pip`

Run the following command to install Django and all other project requirements:  
`$ pip install -r requirements.txt`

### Migrating the Database

You will need to apply all of the database migrations to your SQLite3 database instance.  Navigate to the `mysite` directory (located at the top level of the repository) and issue the following command:  

`$ python manage.py migrate`

### Populating the Database

There is a script located in scheduling/management/commands that adds a few starting items into the database (PreferenceOptions and StudentType).  Run the script:  

`$ python manage.py populate_db`

You are now ready to run the web app!

## Running the Application

### Starting the Virtualenv

Start the virtual environment, if you haven't already:  

**Windows**  
`myvenv\Scripts\activate`

**Linux/OS X**  
`$ source myvenv/bin/activate`

If your console prompt is prefaced with `(myvenv)`, your virtualenv has been activated.

Navigate to the `mysite` directory, located at the top level of the repository.

### Starting the Server

`$ python manage.py runserver`

## Admin Site

The admin site is located at `/admin/`, for example: `http://localhost:8000/admin`.  This is where an administrative user can view and edit database models.  In order to access the admin site, the authenticated user must have superuser status.  

Although a user can be upgraded to superuser status from the admin site, this is not helpful until you have at least one user with superuser status :)  Fortunately, a user can be upgraded to superuser status from the Django shell.

### Upgrading to Superuser Status

Make sure your virtualenv is started (see **Running the Application**). In the top-level `mysite` directory, start the Django shell:  

`$ python manage.py shell`  

Once the interactive console has started, fetch your User from the database:  

```
from scheduling.models import User  
user = User.objects.get(username="myname")
user.is_staff = True
user.is_teacher = True
user.is_superuser = True
user.save()
quit()
```

You should now be able to log into the admin site using the User account you just upgraded.

### Managing from Admin

Some of the functionality of the app is only available from the admin portal.  You will need to use the admin portal to manage StudentTypes, SchedulingRequirements, PreferenceOptions, and User permissions.

**StudentTypes**  
The populate_db script that we ran when setting up the app will add one Student Type - "Other".  You will need to manually add in any other StudentTypes that you would like.  These are the options that students will be choose from them when they first set up their account.

**SchedulingRequirements**  
Once you've created a Room, you will need to create a SchedulingRequirement from each StudentType that will be included in the Room.  This represents the number of hours that the student is required to work in the Room.

**PreferenceOptions**  
These are the options that students have to choose from when submitting their preferences, along with the color coding used in the website.

**User Permissions**
You will need to use the admin portal to upgrade a student to a teacher or admin.

## Updating the Database
To make any updates to the database models, edit the `models.py` file and save.  Then, you will need to create the migrations file:  

`$ python manage.py makemigrations`  

Next, run the migrations;

`$ python manage.py migrate`

If you added a new model and would like to be able to manage it from the admin site, you will need to register it.  In `admin.py` located within the `scheduling` directory, add the following line:  

`admin.site.register(<ModelName>)`

## Views

The <a href="https://docs.djangoproject.com/en/2.2/topics/http/views/">Views</a> are located in `scheduling/views`.  A View is simply a Python function that takes a web request and returns a web response.  The Views are responsible for rendering the HTML templates.  There are three namespaces: scheduling, students, and teachers.  The students and teachers namespaces contain Views that are specific to students and teachers, respectively.  The scheduling namespace contains Views that are not specific to either students or teachers.

### Database API

The Views make several queries using the <a href="https://docs.djangoproject.com/en/2.2/topics/db/queries/">Django Database API</a>.  The API provides a convenient layer of abstraction for interacting with the Django models.

### Decorators

Access to Views is managed using <a href="https://docs.djangoproject.com/en/2.2/topics/http/decorators/">View decorators</a>.
Views with the @login_required decorator can only be accessed by an authenticated user, Views with the @teacher_required can only be accessed by a user with `is_teacher == True`.  The decorators can be manage from `decorators.py` in the scheduling directory.  Make sure you add the appropriate decorators to any new Views you create.

## Common Problems

When I try to run any `manage.py` commands, I get the following error:  

```
  File "manage.py", line 14
    ) from exc
         ^
```

**Solution**:  
Make sure your virtual environment has been started (see **Running the Application** section).
