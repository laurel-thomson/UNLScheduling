from django.views.generic import ListView

from ..models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'scheduling/teachers/room_list.html'

    def get_queryset(self):
        return Room.objects.all()