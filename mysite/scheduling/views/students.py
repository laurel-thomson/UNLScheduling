from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django import forms
import logging
from django.contrib import messages

from ..forms import StudentSignUpForm
from ..models import *
from ..decorators import student_required

logger = logging.getLogger(__name__)

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
    room = get_object_or_404(Room, pk=room_id)

    if (term.schedule_completed):
        return finalized_schedule(request, room, term)
    else:
        return unfinalized_schedule(request, room, term)

def finalized_schedule(request, room, term):
    time_slots = term.timeslot_set.all()
    schedule = {}
    for slot in time_slots:
        schedule[slot] = slot.scheduleduser_set.all()
    return render(request, 'scheduling/students/finalized_schedule.html', {'room': room, 'term':term, 'schedule':schedule})

def unfinalized_schedule(request, room, term):
    if request.method == 'POST':
        slots = term.timeslot_set.all()
        for slot in slots:
            pref_option = get_object_or_404(PreferenceOption, name = request.POST.get(str(slot.id)))
            SchedulePreference.objects.update_or_create(time_slot_id = slot, user_id = request.user, defaults = {'preference_id': pref_option})
        messages.success(request, 'Changes successfully saved.')
        return HttpResponseRedirect('')
    else:
        time_slots = term.timeslot_set.all()
        schedule = {}
        for slot in time_slots:
            prefs = slot.schedulepreference_set.filter(user_id = request.user.id)
            if (len(prefs) > 0):
                schedule[slot] = prefs[0]
            else:
                schedule[slot] = None
        options = PreferenceOption.objects.all()

        return render(request, 'scheduling/students/unfinalized_schedule.html', {'room': room, 'schedule': schedule, 'options': options})