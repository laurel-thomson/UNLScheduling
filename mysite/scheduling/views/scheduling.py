from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from ..models import Room, RoomTerm, TimeSlot, User

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def index(request):
    # if request.user.is_authenticated:
    #     if request.user.is_teacher:
    #         return redirect('students/')
    #     else:
    #         return redirect('teachers/')
    return render(request, 'scheduling/index.html')

def room_detail(request, room_id):
    terms = RoomTerm.objects.filter(room_id=room_id)
    room = get_object_or_404(Room, pk=room_id)
    users = User.objects.filter(roomprivilege__room_id = room_id)
    return render(request, 'scheduling/room_detail.html', {'terms': terms, 'room': room, 'users': users})

def term_schedule(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    time_slots = term.timeslot_set.all()
    schedule = {}

    if (term.schedule_completed):
        for slot in time_slots:
            schedule[slot] = slot.scheduleduser_set.all()
        return render(request, 'scheduling/finalized_schedule.html', {'term':term, 'schedule':schedule})
    else:
        for slot in time_slots:
            schedule[slot] = slot.schedulepreference_set.all()
        return render(request, 'scheduling/unfinalized_schedule.html', {'term':term, 'schedule':schedule})