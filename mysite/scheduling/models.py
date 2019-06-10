from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username

#The type of student (graduate, undergraduate, etc.)
class StudentType(models.Model):
    name = models.CharField('Student Type Name', max_length = 100)

    def __str__(self):
        return self.name

class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    student_type = models.ForeignKey(StudentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username

class Room(models.Model):
    name = models.CharField('Name', max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class RoomTerm(models.Model):
    name = models.CharField('Name', max_length=50)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    available_until = models.DateTimeField()
    schedule_completed = models.BooleanField('Schedule completed', default=False)

    def __str__(self):
        return self.name

#The scheduling requirements for a specific term for a type of student (for example: undergraduate students in Spring 2019 need to sign up for 6 time slots)
class ScheduleRequirement(models.Model):
    term_id = models.ForeignKey(RoomTerm, on_delete=models.CASCADE)
    student_type = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    minimum_slots = models.IntegerField()

class TimeSlot(models.Model):
    day = models.CharField('Day', max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_term_id = models.ForeignKey(RoomTerm, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} - {}".format(self.day, self.start_time, self.end_time)

class ScheduledUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot_id = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.user_id, self.time_slot_id)

class SchedulePreference(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot_id = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    preference_type = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(self.user_id, self.time_slot_id)

class RoomPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    privilege_level = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(self.user_id, self.room_id)