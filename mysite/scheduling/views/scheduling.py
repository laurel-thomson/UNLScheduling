from django.shortcuts import render
from django.views.generic import ListView

from ..models import Room, RoomTerm

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