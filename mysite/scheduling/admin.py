from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import *

admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomTerm)
admin.site.register(TimeSlot)
admin.site.register(ScheduledUser)
admin.site.register(SchedulePreference)
admin.site.register(RoomPrivilege)
admin.site.register(Student)
admin.site.register(StudentType)
admin.site.register(ScheduleRequirement)