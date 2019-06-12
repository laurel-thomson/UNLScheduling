from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib import messages
import logging
import datetime

from ..forms import TeacherSignUpForm, RoomForm, TermForm, TimeSlotForm
from ..models import *
from ..decorators import teacher_required

logger = logging.getLogger(__name__)

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
def term_list(request, room_id):
    get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    room = get_object_or_404(Room, pk=room_id)
    terms = RoomTerm.objects.filter(room_id=room_id)
    form = TermForm()
    return render(request, 'scheduling/teachers/term_list.html', {'terms': terms, 'room': room, 'form': form})

@login_required
@teacher_required
def create_term(request, room_id):
    get_object_or_404(RoomPrivilege, room_id=room_id, user_id=request.user.id)
    room = get_object_or_404(Room, pk=room_id)
    term = RoomTerm(room_id = room, schedule_completed=False)
    form = TermForm(request.POST, instance=term)
    form.save()
    return redirect('/scheduling/teachers/{}/'.format(room_id))

@login_required
@teacher_required
def user_list(request, room_id):
    get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        user_id = request.POST.get('users')
        user = get_object_or_404(User, pk=user_id)
        privilege = RoomPrivilege(user_id = user, room_id=room, privilege_level = 1)
        privilege.save()
        return HttpResponseRedirect('')
    else:
        students = User.objects.filter(roomprivilege__room_id = room_id, is_student = True)
        unprivileged_users = User.objects.exclude(roomprivilege__room_id = room_id).exclude(is_superuser = True)
        terms = room.roomterm_set.all()

        user_data = {}
        for term in terms:
            user_data[term] = {}
            for user in students:
                user_data[term][user] = {}
                user_data[term][user]["submitted_preferences"] = SchedulePreference.objects.filter(user_id = user.id, time_slot_id__room_term_id = term.id).exists()
                user_data[term][user]["was_scheduled"] = ScheduledUser.objects.filter(user_id = user.id, time_slot_id__room_term_id = term.id).exists()
        logger.error(user_data)
        return render(request, 'scheduling/teachers/user_list.html', {'room': room, 'unprivileged_users': unprivileged_users, 'user_data': user_data})

@login_required
@teacher_required
def term_detail(request, room_id, term_id):
    get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    term = get_object_or_404(RoomTerm, pk=term_id)

    if (term.schedule_completed):
        return finalized_schedule(request, term)
    else:
        return unfinalized_schedule(request, term)

def finalized_schedule(request, term):
    time_slots = term.timeslot_set.all()
    room = term.room_id
    schedule = {}
    for slot in time_slots:
        schedule[slot] = slot.scheduleduser_set.all()
    return render(request, 'scheduling/teachers/finalized_schedule.html', {'room':room,'term':term, 'schedule':schedule})

def unfinalized_schedule(request, term):
    time_slots = term.timeslot_set.all()
    room = term.room_id
    form = TimeSlotForm()

    schedule = {}
    users = User.objects.filter(roomprivilege__room_id = room.id, is_student = True)
    for slot in time_slots:
        schedule[slot] = {}
        for user in users:
            try:
                pref = SchedulePreference.objects.get(user_id = user.id, time_slot_id = slot.id)
                option = pref.preference_id
                if (option.color_coding):
                    schedule[slot][user] = {}
                    schedule[slot][user]["preference"] = option
                    schedule[slot][user]["is_scheduled"] = ScheduledUser.objects.filter(user_id = user.id, time_slot_id = slot.id).exists()
            except:
                pass
    options = PreferenceOption.objects.filter(color_coding__isnull=False)
    return render(request, 'scheduling/teachers/unfinalized_schedule.html', {'room':room,'term':term, 'schedule':schedule, 'form': form, 'options': options})

@login_required
@teacher_required
def update_schedule(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    time_slots = term.timeslot_set.all()
    users = User.objects.filter(roomprivilege__room_id = room_id, is_student = True)

    for slot in time_slots:
        for user in users:
            to_be_scheduled = request.POST.get("{}_{}".format(slot.id,user.id)) == 'on'
            if to_be_scheduled:
                if not ScheduledUser.objects.filter(user_id = user.id, time_slot_id = slot.id).exists():
                    s_user = ScheduledUser(user_id = user, time_slot_id = slot)
                    s_user.save()
            else:
                if ScheduledUser.objects.filter(user_id = user.id, time_slot_id = slot.id).exists():
                    s_user = get_object_or_404(ScheduledUser, user_id = user.id, time_slot_id=slot.id)
                    s_user.delete()
    messages.success(request, 'Changes successfully saved.')
    return redirect('/scheduling/teachers/{}/{}/'.format(room_id, term_id))

@login_required
@teacher_required
def add_time_slot(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    time_slot = TimeSlot(room_term_id = term)
    form = TimeSlotForm(request.POST, instance=time_slot)
    form.save()
    return redirect('/scheduling/teachers/{}/{}/'.format(room_id, term_id))

@login_required
@teacher_required
def create_room(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        room = Room(owner=user)
        form = RoomForm(request.POST, instance=room)
        form.save()
        privilege = RoomPrivilege(user_id = user, room_id = room, privilege_level = 2)
        privilege.save()
        return redirect('/scheduling/teachers/')
    else:
        form = RoomForm()
        return render(request, 'scheduling/teachers/create_update_room.html', {'form': form})

@login_required
@teacher_required
def delete_room(request, room_id):
    #send a 404 if the user deleting isn't the owner of the room
    room = get_object_or_404(Room,pk=room_id, owner=request.user.id)
    room.delete()
    return redirect('/scheduling/teachers/')

@login_required
@teacher_required
def delete_term(request, room_id, term_id):
    get_object_or_404(RoomPrivilege, room_id = room_id, user_id = request.user.id)
    term = get_object_or_404(RoomTerm, pk=term_id)
    term.delete()
    return redirect('/scheduling/teachers/{}'.format(room_id))

@login_required
@teacher_required
def remove_user(request, room_id, user_id):
    privilege = get_object_or_404(RoomPrivilege, room_id=room_id, user_id=user_id)
    privilege.delete()
    return redirect('/scheduling/teachers/{}/users'.format(room_id))

@login_required
@teacher_required
def finalize_schedule(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    term.schedule_completed = True
    term.save()
    return redirect('/scheduling/teachers/{}/{}'.format(room_id, term_id))

@login_required
@teacher_required
def unfinalize_schedule(request, room_id, term_id):
    term = get_object_or_404(RoomTerm, pk=term_id)
    term.schedule_completed = False
    term.save()
    return redirect('/scheduling/teachers/{}/{}'.format(room_id, term_id))

@login_required
@teacher_required
def delete_time_slot(request, room_id, term_id, slot_id):
    get_object_or_404(RoomPrivilege, user_id = request.user.id, room_id = room_id)
    slot = get_object_or_404(TimeSlot, pk=slot_id)
    slot.delete()
    return redirect('/scheduling/teachers/{}/{}'.format(room_id, term_id))