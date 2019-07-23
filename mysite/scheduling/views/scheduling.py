from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
import logging

from ..models import Room, RoomTerm, TimeSlot, User
from ..forms import SignUpForm

logger = logging.getLogger(__name__)

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers/')
        else:
            return redirect('students/')
    return render(request, 'scheduling/index.html')

def onLogin(tree):
    username = tree[0][0].text
    user = User.objects.get(pk=username)

    #If the user hasn't added in their information yet, prompt them to
    if (not user.first_name):
        return redirect('signup/')
    else:
        return redirect('')
        

def signup(request):
    if (request.method == 'POST'):
        return index(request)
    else:
        form = SignUpForm()
        return render(request, 'scheduling/signup.html', {'form': form})