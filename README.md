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
Download or clone the repository and navigate to the root directory of the repo.  Make a virtualenv called myvenv that will isolate your Python/Django setup:  

`$ python3 -m venv myvenv`

Start your virtualenv:

**Windows**  
`$ myvenv\Scripts\activate`

**Linux/OS X**  
`$ source myvenv/bin/activate`

If your virtualenv has been successfully activated, your console prompt will be prefaced with `(myvenv)`.

### Installing Requirements
Make sure that pip is up-to-date:  
`python -m pip install --upgrade pip`

Run the following command to install Django and all other project requirements:  
`pip install -r requirements.txt`

### Migrating the database

You will need to apply all of the database migrations to your SQLite3 database instance:  

`python manage.py migrate`

You are now ready to run the web app!

## Running the Application

### Starting the Virtualenv

Start the virtual environment, if you haven't already:  

**Windows**  
`$ myvenv\Scripts\activate`

**Linux/OS X**  
`$ source myvenv/bin/activate`

If your console prompt is prefaced with `(myvenv)`, your virtualenv has been activated.

Navigate to the mysite directory, located at the top level of the repository.

### Starting the Server

`python manage.py runserver`
