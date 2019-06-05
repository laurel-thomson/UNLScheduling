from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from ..models import Room, RoomTerm, TimeSlot, User

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers/')
        else:
            return redirect('students/')
    return render(request, 'scheduling/index.html')