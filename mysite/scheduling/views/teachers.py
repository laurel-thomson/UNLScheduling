from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib import messages
import logging
import datetime
import csv

from ..forms import RoomForm, TermForm, TimeSlotForm, UploadTimeSlotsForm
from ..models import *
from ..decorators import teacher_required

logger = logging.getLogger(__name__)

@login_required
@teacher_required
def room_list(request):
    rooms = Room.objects.filter(roomprivilege__user_id = request.user.id)
    form = RoomForm()
    return render(request, 'scheduling/teachers/room_list.html', {'rooms': rooms, 'form': form})

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
    if (request.method == 'POST'):
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
    students = User.objects.filter(roomprivilege__room_id = room_id, is_student = True)
    teachers = User.objects.filter(roomprivilege__room_id = room.id, is_teacher = True)
    unprivileged_users = User.objects.exclude(roomprivilege__room_id = room_id).exclude(is_superuser = True).order_by("is_student")
    terms = room.roomterm_set.all()

    student_data = {}
    for term in terms:
        student_data[term] = {}
        for user in students:
            student_data[term][user] = {}
            student_data[term][user]["slots_submitted"] = SchedulePreference.objects.filter(user_id = user.id, time_slot_id__room_term_id = term.id).exclude(preference_id__name = 'Not Available').count()
            student_data[term][user]["was_scheduled"] = ScheduledUser.objects.filter(user_id = user.id, time_slot_id__room_term_id = term.id).exists()
            student_data[term][user]["student_type"] = get_object_or_404(Student, pk = user.id).student_type
            if ScheduleRequirement.objects.filter(room_id = room.id, student_type = student_data[term][user]["student_type"].id).exists():
                student_data[term][user]["minimum_slots"] = get_object_or_404(ScheduleRequirement, room_id = room.id, student_type = student_data[term][user]["student_type"].id)
    return render(request, 'scheduling/teachers/user_list.html', {'room': room, 'unprivileged_users': unprivileged_users, 'student_data': student_data, 'teachers': teachers})

@login_required
@teacher_required
def add_users_to_room(request, room_id):
    get_object_or_404(RoomPrivilege, user_id=request.user.id, room_id=room_id)
    if request.method == 'POST':
        unprivileged_users = User.objects.exclude(roomprivilege__room_id = room_id).exclude(is_superuser = True)
        for user in unprivileged_users:
            if request.POST.get(str(user.id)) == 'on':
                room = get_object_or_404(Room, pk=room_id)
                privilege = RoomPrivilege(user_id = user, room_id=room)
                privilege.save()
        messages.success(request, "Users successfully added.")
        return redirect('/scheduling/teachers/{}/users'.format(room_id))

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
    single_add_form = TimeSlotForm()
    file_upload_form = UploadTimeSlotsForm()

    schedule = {}
    users = User.objects.filter(roomprivilege__room_id = room.id, is_student = True)
    for slot in time_slots:
        schedule[slot] = {}
        for user in users:
            try:
                pref = SchedulePreference.objects.get(user_id = user.id, time_slot_id = slot.id)
                option = pref.preference_id
                if (option.name != 'Not Available'):
                    schedule[slot][user] = {}
                    schedule[slot][user]["preference"] = option
                    schedule[slot][user]["is_scheduled"] = ScheduledUser.objects.filter(user_id = user.id, time_slot_id = slot.id).exists()
            except:
                pass
    options = PreferenceOption.objects.exclude(name='Not Available')
    requirements = {}
    for user in users:
        try:
            student = Student.objects.get(user_id = user.id)
            requirements[user.id] = ScheduleRequirement.objects.get(room_id = room.id, student_type = student.student_type).minimum_slots
        except:
            requirements[user.id] = -1
    return render(request, 'scheduling/teachers/unfinalized_schedule.html', 
        {'room':room, 'term':term, 'schedule':schedule, 'single_add_form': single_add_form, 'options': options, 'requirements': requirements, 'file_upload_form': file_upload_form})

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
    if (request.method == 'POST'):
        term = get_object_or_404(RoomTerm, pk=term_id)
        time_slot = TimeSlot(room_term_id = term)
        form = TimeSlotForm(request.POST, instance=time_slot)
        form.save()
        return redirect('/scheduling/teachers/{}/{}/'.format(room_id, term_id))

@login_required
@teacher_required
def import_time_slots_file(request, room_id, term_id):
    if request.method == 'POST' and request.FILES['file']:
        try:
            term = RoomTerm.objects.get(pk=term_id)
            file = request.FILES['file'] 
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for line in reader:
                day = line["day"]
                start_time = line["start_time"]
                end_time = line["end_time"]
                time_slot = TimeSlot(room_term_id=term, day=day, start_time=start_time, end_time=end_time)
                time_slot.save()
            messages.success(request, 'Time slots successfully imported.')
            return redirect('/scheduling/teachers/{}/{}'.format(room_id, term_id))
        except Exception as e:
            logger.error("Exception = {}".format(str(e)))
            messages.error(request, 'There was an error processing your file.')
            return redirect('/scheduling/teachers/{}/{}'.format(room_id, term_id))

@login_required
@teacher_required
def create_room(request):
    if (request.method == 'POST'):
        user = User.objects.get(pk=request.user.id)
        room = Room(owner=user)
        form = RoomForm(request.POST, instance=room)
        form.save()
        privilege = RoomPrivilege(user_id = user, room_id = room)
        privilege.save()
        return redirect('/scheduling/teachers/')

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
    messages.success(request, "User successfully removed from room")
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