from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from ..forms import TeacherSignUpForm
from ..models import Room, RoomTerm, TimeSlot, User
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