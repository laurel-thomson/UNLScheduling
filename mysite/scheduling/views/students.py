from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Room, RoomTerm, TimeSlot, User
from ..decorators import student_required

app_name = 'students'

@login_required
@student_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'scheduling/students/room_list.html', {'rooms': rooms})