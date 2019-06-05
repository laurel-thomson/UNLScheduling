from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django import forms

from ..forms import StudentSignUpForm
from ..models import Room, RoomTerm, TimeSlot, User, RoomPrivilege
from ..decorators import student_required

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/scheduling/students/')


@login_required
@student_required
def room_list(request):
    rooms = Room.objects.filter(roomprivilege__user_id = request.user.id)
    return render(request, 'scheduling/students/room_list.html', {'rooms': rooms})

@login_required
@student_required
def room_detail(request, room_id):
    #check if the user has privilege for the room - 404 if not
    privilege = get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    terms = RoomTerm.objects.filter(room_id=room_id)
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'scheduling/students/room_detail.html', {'terms': terms, 'room': room })
    
@login_required
@student_required
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
    return render(request, 'scheduling/students/finalized_schedule.html', {'term':term, 'schedule':schedule})

def unfinalized_schedule(request, term):
    if request.method == 'POST':
        #get data from form
        return redirect('/scheduling/students/')
    else:
        time_slots = term.timeslot_set.all()
        schedule = {}
        for slot in time_slots:
            prefs = slot.schedulepreference_set.filter(user_id = request.user.id)
            if (len(prefs) > 0):
                schedule[slot] = prefs[0]
            else:
                schedule[slot] = None

        return render(request, 'scheduling/students/unfinalized_schedule.html', {'schedule': schedule})