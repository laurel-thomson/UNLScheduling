from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from ..forms import TeacherSignUpForm
from ..models import Room, RoomTerm, TimeSlot, User, RoomPrivilege
from ..decorators import teacher_required


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/scheduling/teachers/')

@login_required
@teacher_required
def room_list(request):
    rooms = Room.objects.filter(roomprivilege__user_id = request.user.id)
    return render(request, 'scheduling/teachers/room_list.html', {'rooms': rooms})

@login_required
@teacher_required
def room_detail(request, room_id):
    #check if the user has privilege for the room - 404 if not
    privilege = get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    terms = RoomTerm.objects.filter(room_id=room_id)
    room = get_object_or_404(Room, pk=room_id)
    users = User.objects.filter(roomprivilege__room_id = room_id)
    return render(request, 'scheduling/teachers/room_detail.html', {'terms': terms, 'room': room, 'users': users})

@login_required
@teacher_required
def term_detail(request, room_id, term_id):
    #check if the user has privilege for the room - 404 if not
    privilege = get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)

    term = get_object_or_404(RoomTerm, pk=term_id)

    if (term.schedule_completed):
        return finalized_schedule(request, term)
    else:
        return unfinalized_schedule(request, term)

def finalized_schedule(request, term):
    time_slots = term.timeslot_set.all()
    schedule = {}
    for slot in time_slots:
        schedule[slot] = slot.scheduleduser_set.all()
    return render(request, 'scheduling/teachers/finalized_schedule.html', {'term':term, 'schedule':schedule})

def unfinalized_schedule(request, term):
    time_slots = term.timeslot_set.all()
    schedule = {}
    for slot in time_slots:
        schedule[slot] = slot.schedulepreference_set.all()
    return render(request, 'scheduling/teachers/unfinalized_schedule.html', {'term':term, 'schedule':schedule})