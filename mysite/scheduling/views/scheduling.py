from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from ..models import Room, RoomTerm, TimeSlot, User
from ..forms import SignUpForm

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
    try:
        User.objects.get(username=username)
        return redirect('')
    except:
        return redirect('signup/')
        

def signup(request):
    if (request.method == 'POST'):
        #save the user info here
        pass
    else:
        form = SignUpForm()
        return render(request, 'scheduling/signup.html', {'form': form})