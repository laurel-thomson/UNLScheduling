from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Room(models.Model):
    name = models.CharField('Name', max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class RoomTerm(models.Model):
    name = models.CharField('Name', max_length=50)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    available_until = models.DateTimeField()
    schedule_completed = models.BooleanField('Schedule completed', default=False)

class TimeSlot(models.Model):
    day = models.CharField('Day', max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_term_id = models.ForeignKey(RoomTerm, on_delete=models.CASCADE)

class ScheduledUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot_id = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

class SchedulePreference(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot_id = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    preference_type = models.IntegerField()

class RoomPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    privilege_level = models.IntegerField()