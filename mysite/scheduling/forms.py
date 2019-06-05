from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class SubmitTimePreferenceForm(forms.Form):
    is_bound = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schedule = args[0]
        for slot, pref in schedule.items():
            self.fields[slot] = forms.BooleanField(required=False, initial=True)