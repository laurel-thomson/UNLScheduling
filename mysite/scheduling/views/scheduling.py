from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from ..models import Room, RoomTerm, TimeSlot

def index(request):
    return render(request, 'scheduling/index.html')

class RoomListView(ListView):
    model = Room
    template_name = 'scheduling/room_list.html'

    def get_queryset(self):
        return Room.objects.all()

class TermListView(ListView):
    model = RoomTerm
    template_name = 'scheduling/term_list.html'

    def get_queryset(self):
        room = self.kwargs['room_id']
        return RoomTerm.objects.filter(room_id=room)

def term_schedule(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    time_slots = term.timeslot_set.all()

    schedule = {}
    for slot in time_slots:
        schedule[slot] = slot.scheduleduser_set.all()

    return render(request, 'scheduling/term_schedule.html', {'term':term, 'schedule':schedule})