# UNL Scheduling Website

This is a scheduling application created for Dr. Josh Brummer from the University of Nebraska, Lincoln Mathematics Department.  The purpose
of the web app is to streamline the process of scheduling students to work in the UNL Math Resource Center.  The website allows students
to mark their availability and scheduling preferences for each time slot in the resource center.  Teachers can then view a master scheduling
list, where each time slots contains all of the students that have marked that time slots as "available".  The teacher can then 
select which student(s) to schedule for the particular time slot.  Once the teacher releases the schedule, students are able to view
the published schedule.

One of the main benefits of the application is that it simplifies the process of keeping track of how many hours a student has been scheduled
for.  Different students have different scheduling requirements: graduate students work 2 slots per week, some undergraduates work 10
slots per week, others work 6, etc.  When a teacher schedules a student and they meet their scheduling requirement, all of the other
instances where that student can be scheduled are disabled until one of their slots are unscheduled.  This prevents a student from being
over or under scheduled.  Additionally, the web app allows teachers to view data on which students have submitted their preferences and
which have been scheduled.

Finally, this application was created with the intention that it could be expanded for use beyond the Math Resource Center.  Teachers in the
app can create different "rooms" with their own set of students and time slots and use the website to schedule these rooms or events.

A test version of the website is available for viewing <a href="http://http://laurelthomson.pythonanywhere.com">here</a>!

To view the test data that has already been entered, you can log in with a few of these dummy accounts:

username: teacher  
password: mypassword  


username: student1  
password: mypassword


username: student2  
password: mypassword
