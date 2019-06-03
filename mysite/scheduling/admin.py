from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import User, Room, RoomTerm, TimeSlot, ScheduledUser, SchedulePreference, RoomPrivilege

admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomTerm)
admin.site.register(TimeSlot)
admin.site.register(ScheduledUser)
admin.site.register(SchedulePreference)
admin.site.register(RoomPrivilege)